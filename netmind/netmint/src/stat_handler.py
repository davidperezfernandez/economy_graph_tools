#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==========================================
#   Libraries and Packages
from collections import OrderedDict 
import math
import functools
# ==========================================

class StatsHandler:

    def __init__(self,name):

        # debug - for KS and R squared that cannot be computed via python
        self.period     = name
        self.directory     = "output/extra_matlab/"
        self.ks     = []
        self.r_squared     = []



    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # -------------------------------------------------------------

    def get_distribution_info(self, distribution):

        [mean,sd,skewness,kurtosis]    = self.get_mean_sd_etc(distribution)
        hhi                         = self.hhi(distribution)
        distribution_list             = sorted (distribution.values())
        percentiles                 = []
        i = 90
        while (i>5):
            percentiles.append(self.percentile(distribution_list, float(i)/100))
            i -= 10
        percentiles.append(self.percentile(distribution_list, 0.05))
        percentiles.append(self.percentile(distribution_list, 0.01))

        return [mean, sd, skewness, kurtosis, hhi, percentiles]

    # -------------------------------------------------------------
    # 
    #  get_cumulative_distribution(distribution)
    # 
    # -------------------------------------------------------------

    def compute_cumulative_distribution(self, distribution):

            cdf = []
            cdf.append(0.0)
            psum = float(sum(distribution))
            for i in range(0,len(distribution)):
                cdf.append(cdf[i]+distribution[i]/psum)
            del cdf[0]
            for i in range(len(cdf)):
                cdf[i] = 1 - cdf[i]
            cdf[len(cdf)-1]=0
            return cdf

    # -------------------------------------------------------------
    # 
    #  get_cumulative_distribution(distribution_dictionary, aggregate_number)
    # 
    #             INPUT: - dictionary with entity as key and feature as value
    #                    
    # [- aggregate number 
    #                                 - if the cumulative distribution needs 
    #                                 to be computed from an aggregated distribution
    #                                 - =0 else]
    # 
    #             OUTPUT: double list 
    #                         - [0] is the cumulative distribution (probability value)
    #                         - [1] is the corresponding value    
    # 
    # -------------------------------------------------------------

    def get_cumulative_distribution(self, distribution):

            # when more then one data point need to be merged
            # sort by values and combine them accordin to the aggregate number
            # if aggregate_number >1:
            #     distribution = self.aggregate_distribution(distribution_dictionary, aggregate_number)
            # else:
            # distribution = distribution_dictionary

            values  = sorted(set(distribution.values()))
            hist    = [list(distribution.values()).count(x) for x in values]
            cdf     = self.compute_cumulative_distribution(hist)

            return [cdf, values]

    # -------------------------------------------------------------
    # 
    #  get_mean_sd_etc(self, distribution)
    # 
    # -------------------------------------------------------------

    def get_mean_sd_etc(self, distribution):
        
        if isinstance(distribution,dict):
                distribution = distribution.values()
        mean    = float(sum(distribution))/len(distribution)
        sd      = 0.0
        for x in distribution:
            sd += (x-mean)**2
        sd_unsquared = sd / len(distribution)
        sd = sd_unsquared **0.5

        skewness = 0.0
        for x in distribution:
            skewness += (x-mean)**3
        skewness = skewness / ((len(distribution)-1)*sd_unsquared**(float(3)/2))

        kurtosis = 0.0
        for x in distribution:
            kurtosis += (x-mean)**4
        kurtosis = kurtosis / ((len(distribution)-1)*sd_unsquared**(float(4)/2)) - 3

        return [mean,sd,skewness,kurtosis]

    # -------------------------------------------------------------
    # 
    #  percentile
    # Find the percentile of a list of values.
    # @parameter N - is a list of values. Note N MUST BE already sorted.
    # @parameter percent - a float value from 0.0 to 1.0.
    # @parameter key - optional key function to compute value from each element of N.
    # @return - the percentile of the values
    # 
    # -------------------------------------------------------------

    def percentile(self, N, percent, key=lambda x:x):

        percent = 1.0 - percent
        if not N:
            return None
        k = (len(N)-1) * percent
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            perc = key(N[int(k)])
        else:
            d0 = key(N[int(f)]) * (c-k)
            d1 = key(N[int(c)]) * (k-f)
            perc = d0+d1

        return perc

    # -------------------------------------------------------------
    # 
    #  herfindhal-hirschman index
    # 
    # -------------------------------------------------------------

    def hhi(self, distribution):
        if isinstance(distribution,dict):
            distribution = distribution.values()
        total = sum(distribution)
        hhi = 0.0
        for elem in distribution:
            share = float(elem)/total
            share = share*share
            hhi += share
        normed_hhi = (hhi-1.0/len(distribution))/(1.0-1.0/len(distribution))
        return hhi

# -----------------------------------------
# -----------------------------------------
# TODO:
# -----------------------------------------
# -----------------------------------------

    def ks_store(self, distribution, title):
        
        self.ks.append(title)
        distribution = self.get_cumulative_distribution(distribution)[0]
        self.ks.append(distribution)
        # return 0

    def r_square(self, distribution_1, distribution_2, title):
        self.r_squared.append(title)
        self.r_squared.append(distribution_1)
        self.r_squared.append(distribution_2)
        # return -1

    def save_ks_s(self):
        file_ks = open (self.directory+"ks_{0}.csv".format(self.period),'w')
        for line in self.ks:
            if isinstance(line,list):
                string = ','.join(str(e) for e in line)
                file_ks.write(string + '\n')
            else:
                file_ks.write(str(line)+'\n')
        file_ks.close()

        file_r = open (self.directory+"r_squared_{0}.csv".format(self.period),'w')
        for line in self.r_squared:
            if isinstance(line,list):
                string = ','.join(str(e) for e in line)
                file_r.write(string + '\n')
            else:
                file_r.write(str(line)+'\n')
        file_r.close()
