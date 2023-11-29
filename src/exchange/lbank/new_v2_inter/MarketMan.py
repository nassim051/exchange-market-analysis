#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 17:19
# @Author  : maochong
# @File    : MarketMan.py
import src.exchange.lbank.APIV2Excu as APIV2Excu


class MarketMan:
  def __init__(self, key=1):
    self.excuReq = APIV2Excu.APIV2Excu(key)

  def getSystem_ping(self):
    str = self.getSystem_ping.__name__

    par = {}

    self.excuReq.ExcuRequests(par, str)

  def getIncrDepth(self, **d):
    str = self.getIncrDepthV2.__name__
    par = {}
    for key in d.keys():
      par[key] = d[key]

    self.excuReq.ExcuRequests(par, str)

  def getTradesV2(self, **d):
    str = self.getTradesV2.__name__
    par = {}
    for key in d.keys():
      par[key] = d[key]
    return self.excuReq.ExcuRequests(par, str)

  def getPrice(self, **d):
    str = self.getPrice.__name__

    par = {}
    for key in d.keys():
      par[key] = d[key]

    self.excuReq.ExcuRequests(par, str)

  def getBookTicker(self, **d):
    str = self.getBookTicker.__name__

    par = {}
    for key in d.keys():
      par[key] = d[key]

    self.excuReq.ExcuRequests(par, str)