# py-motmetrics - Metrics for multiple object tracker (MOT) benchmarking.
# https://github.com/cheind/py-motmetrics/
#
# MIT License
# Copyright (c) 2017-2020 Christoph Heindl, Jack Valmadre and others.
# See LICENSE file for terms.

"""Compute metrics for trackers using MOTChallenge ground-truth data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from collections import OrderedDict
import glob
import logging
import os
from pathlib import Path

import motmetrics as mm
import numpy as np 
import pandas as pd
from pandas.core.algorithms import isin 


def parse_args():
    """Defines and parses command-line arguments."""
    parser = argparse.ArgumentParser(description="""
Compute metrics for trackers using MOTChallenge ground-truth data.

Files
-----
All file content, ground truth and test files, have to comply with the
format described in

Milan, Anton, et al.
"Mot16: A benchmark for multi-object tracking."
arXiv preprint arXiv:1603.00831 (2016).
https://motchallenge.net/

Structure
---------

Layout for ground truth data
    <GT_ROOT>/<SEQUENCE_1>/gt/gt.txt
    <GT_ROOT>/<SEQUENCE_2>/gt/gt.txt
    ...

Layout for test data
    <TEST_ROOT>/<SEQUENCE_1>.txt
    <TEST_ROOT>/<SEQUENCE_2>.txt
    ...

Sequences of ground truth and test will be matched according to the `<SEQUENCE_X>`
string.""", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--gt_txt', type=str, help=' ground truth files.', default='/workspace/workspace/tracking/py-motmetrics/motmetrics/data/TUD-Campus/gt.txt')
    parser.add_argument('--test_txt', type=str, help=' tracker result files', default='/workspace/workspace/tracking/py-motmetrics/motmetrics/data/TUD-Campus/test.txt')

    parser.add_argument('--solver', type=str, help='LAP solver to use for matching between frames.')
    parser.add_argument('--id_solver', type=str, help='LAP solver to use for ID metrics. Defaults to --solver.')
    parser.add_argument('--exclude_id', dest='exclude_id', default=False, action='store_true',
                        help='Disable ID metrics')
    parser.add_argument('--loglevel', type=str, help='Log level', default='info')
    parser.add_argument('--fmt', type=str, help='Data format', default='mot15-2D')
    return parser.parse_args()


def compare_dataframes(gts, ts):
    """Builds accumulator for each sequence."""
    accs = []
    names = []
    for k, tsacc in ts.items():
        if k in gts:
            logging.info('Comparing %s...', k)
            accs.append(mm.utils.compare_to_groundtruth(gts[k], tsacc, 'iou', distth=0.5))
            names.append(k)
        else:
            logging.warning('No ground truth for %s, skipping.', k)

    return accs, names

def compare_data_txt(gts_txt, dts_txt, distth=0.5, fmt='mot16'):
    # convert gts dts to df 
    df_gts =  mm.io.loadtxt(gts_txt, fmt=fmt, min_confidence=1)
    df_dts =  mm.io.loadtxt(dts_txt, fmt=fmt)
    accs = mm.utils.compare_to_groundtruth(df_gts, df_dts, 'iou', distth=distth)
    mh = mm.metrics.create()
    metrics = list(mm.metrics.motchallenge_metrics)
    metrics = [x for x in metrics if not x.startswith('id')]
    summary = mh.compute_many([accs], metrics=metrics, generate_overall=True)
    print(mm.io.render_summary(summary, formatters=mh.formatters, namemap=mm.io.motchallenge_metric_names))
    return summary

def compare_data_list(gts, dts, distth=0.5, fmt='mot16', conf_ind=6):
    # convert gts dts to df 
    npy_gts =  np.array(gts)
    npy_dts =  np.array(dts)
    assert npy_gts.shape[1]==10 
    assert npy_dts.shape[1]==10
    columns = ['FrameId', 'Id', 'X', 'Y', 'Width', 'Height', 'Confidence', 'ClassId', 'Visibility', 'unused']
    npy_gts = npy_gts[npy_gts[:,6]>=1]
    df_gts = pd.DataFrame(npy_gts, columns=columns).set_index(['FrameId','Id'])
    df_dts = pd.DataFrame(npy_dts, columns=columns).set_index(['FrameId','Id'])
    accs = mm.utils.compare_to_groundtruth(df_gts, df_dts, 'iou', distth=distth)
    mh = mm.metrics.create()
    metrics = list(mm.metrics.motchallenge_metrics)
    metrics = [x for x in metrics if not x.startswith('id')]
    summary = mh.compute_many([accs], metrics=metrics, generate_overall=True)
    print(mm.io.render_summary(summary, formatters=mh.formatters, namemap=mm.io.motchallenge_metric_names))
    return summary

def simpeval(gts, dts, distth=0.5):
    if isinstance(gts, str):
        summary = compare_data_txt(gts, dts, distth=distth)
    elif isinstance(gts, list):
        summary = compare_data_list(gts, dts, distth=distth)
    return summary

def main():
    # pylint: disable=missing-function-docstring
    args = parse_args()

    loglevel = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(loglevel, int):
        raise ValueError('Invalid log level: {} '.format(args.loglevel))
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%I:%M:%S')

    if args.solver:
        mm.lap.default_solver = args.solver

    gtfiles = [args.gt_txt]
    tsfiles = [args.test_txt]

    accs = compare_data_npy(args.gt_txt, args.test_txt)
    accs = compare_data_txt(args.gt_txt, args.test_txt)

    logging.info('Found %d groundtruths and %d test files.', len(gtfiles), len(tsfiles))
    logging.info('Available LAP solvers %s', str(mm.lap.available_solvers))
    logging.info('Default LAP solver \'%s\'', mm.lap.default_solver)
    logging.info('Loading files.')

    gt = OrderedDict([('data_'+ str(i), mm.io.loadtxt(f, fmt=args.fmt, min_confidence=1)) for i, f in enumerate(gtfiles)])
    ts = OrderedDict([('data_'+ str(i), mm.io.loadtxt(f, fmt=args.fmt)) for i,f in enumerate(tsfiles)])
    print(gt.keys())
    print(gt)
    print(ts)

    mh = mm.metrics.create()
    accs, names = compare_dataframes(gt, ts)

    metrics = list(mm.metrics.motchallenge_metrics)
    if args.exclude_id:
        metrics = [x for x in metrics if not x.startswith('id')]

    logging.info('Running metrics')

    if args.id_solver:
        mm.lap.default_solver = args.id_solver
    summary = mh.compute_many(accs, names=names, metrics=metrics, generate_overall=True)
    print(mm.io.render_summary(summary, formatters=mh.formatters, namemap=mm.io.motchallenge_metric_names))
    logging.info('Completed')


if __name__ == '__main__':
    main()
