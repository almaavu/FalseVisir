#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""



CFG = dict(
    
    downsize = 500,

    preprocess_images = dict(
        blur_sigma = 2,
        # equalize = True, # same speed, same results?
        equalize = False,
        normalize = False, # same speed, same results?
        # normalize = False, 
        # edge = True,  # faster
        edge = False,  # better results? 
        edge_sigma = 2,   
        edge_low_threshold = 0.05,
        edge_high_threshold = 0.1,
        ),


    extract_features = dict(
        method='HARRIS',  
        # method='ORB', 
        min_distance = 1,
        threshold_rel = 1e-7,
        patch_size=59,
        ),

    ransac = dict(
        residual_threshold = 10,   # higher - more good matches will be found, longer time?
        min_samples = 5,
        max_trials = 10000,
        ),

    match = dict(
        max_distance = 200,
        ), 
    
    irr_weight = .5,


    model_robust_param_limits = [  # detect excessive transformation
                                    [    [-10,-1,-100],
                                          [-1,-2,-100],
                                          [-0.1,-0.02,0]     ],
                                     [    [10,1,100],
                                          [1,2,100],
                                          [0.1,0.02,2]    ]    
                                     ]
    )
