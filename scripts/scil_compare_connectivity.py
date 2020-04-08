#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Performs a network-based statistical comparison for populations X and Y using
a t-statistic threshold of alpha. All matrices must have the same shape and be
ordered in the same way.

For more details visit:
https://brainconn.readthedocs.io/en/latest/generated/brainconn.nbs.nbs_bct.html
"""

import argparse
import logging

import bct
import numpy as np

from scilpy.io.utils import (add_overwrite_arg, add_verbose_arg,
                             assert_inputs_exist,
                             load_matrix_in_any_format)


EPILOG = """
References:
    [1] Rubinov, Mikail, and Olaf Sporns. "Complex network measures of brain
        connectivity: uses and interpretations." Neuroimage 52.3 (2010):
        1059-1069.
"""


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=EPILOG)

    p.add_argument('--in_g1', nargs='+', required=True,
                   help='')
    p.add_argument('--in_g2', nargs='+', required=True,
                   help='')

    p.add_argument('--t_value', type=float, default=3,
                   help='')
    p.add_argument('--nb_permutations', type=int, default=1000,
                   help='')
    p.add_argument('--tail', choices=['left', 'right', 'both'], default='both',
                   help='')
    p.add_argument('--paired', action='store_true',
                   help='')
    p.add_argument('--filtering_mask',
                   help='Binary filtering mask to apply before computing the '
                        'measures.')
    add_verbose_arg(p)
    add_overwrite_arg(p)

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    assert_inputs_exist(parser, args.in_g1+args.in_g2,
                        args.filtering_mask)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.filtering_mask:
        filtering_mask = load_matrix_in_any_format(args.filtering_mask)
    else:
        filtering_mask = 1
    matrices_g1 = [load_matrix_in_any_format(i)*filtering_mask
                   for i in args.in_g1]
    matrices_g2 = [load_matrix_in_any_format(i)*filtering_mask
                   for i in args.in_g2]
    matrices_g1 = np.rollaxis(np.array(matrices_g1),
                              axis=0, start=3)
    matrices_g2 = np.rollaxis(np.array(matrices_g2),
                              axis=0, start=3)
    pval, _, _ = bct.nbs.nbs_bct(matrices_g1, matrices_g2,
                                 thresh=args.t_value,
                                 k=args.nb_permutations,
                                 tail=args.tail,
                                 paired=args.paired,
                                 verbose=args.verbose)

    print('The statistical significance (pvalue) of the difference between '
          'both group is {}'.format(round(pval, 5)))


if __name__ == '__main__':
    main()
