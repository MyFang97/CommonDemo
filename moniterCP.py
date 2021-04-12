# -*- coding: utf-8 -*-
"""
    gps串口解析
"""
import json
import logging
import threading
import subprocess
import sys
import signal
import os
import time

import requests
import serial
import re

g_runPidMap = {}

g_webGpsUrl = 'http://jc.visualdeep.com:18200/CityInspectors/sendGps.json'
g_webWifiUrl = 'http://jc.visualdeep.com:18200/CityInspectors/sendWifiProbe.json'

g_lastGPSData = {}


def getGPSData():
    global g_lastGPSData
    try:
        if g_lastGPSData != None:
            if g_lastGPSData.has_key('lat'):
                if g_lastGPSData['lat'] == None:
                    g_lastGPSData['lat'] = '0'
            else:
                g_lastGPSData['lat'] = '0'
            if g_lastGPSData.has_key('lon'):
                if g_lastGPSData['lon'] == None:
                    g_lastGPSData['lon'] = '0'
            else:
                g_lastGPSData['lon'] = '0'
            if g_lastGPSData.has_key('lat_ns'):
                if g_lastGPSData['lat_ns'] == None:
                    g_lastGPSData['lat_ns'] = 'N'
            else:
                g_lastGPSData['lat_ns'] = 'N'
            if g_lastGPSData.has_key('lon_ew'):
                if g_lastGPSData['lon_ew'] == None:
                    g_lastGPSData['lon_ew'] = 'E'
            else:
                g_lastGPSData['lon_ew'] = 'E'
            return g_lastGPSData
        else:
            g_lastGPSData['lat'] = '0'
            g_lastGPSData['lon'] = '0'
            g_lastGPSData['lat_ns'] = 'N'
            g_lastGPSData['lon_ew'] = 'E'
            return g_lastGPSData
    except Exception:
        g_lastGPSData['lat'] = '0'
        g_lastGPSData['lon'] = '0'
        g_lastGPSData['lat_ns'] = 'N'
        g_lastGPSData['lon_ew'] = 'E'
    return g_lastGPSData


class GpsParser:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        self.port = port
        self.baud = baudrate
        self.timeout = timeout
        self.GpsUart = serial.Serial(port, baudrate, timeout=timeout)
        self.GpsUart.flush()
        self.read()

    def messageType(self, message):
        # $GPGGA,,,,,,0,00,99.99,,,,,,*48
        checksum = self.checkDataSum(message)
        if checksum is False:
            return None
        if re.match(r'\$GPGGA', message):
            return 'GPGGA'
        elif re.match(r'\$GPRMC', message):
            return 'GPRMC'
        elif re.match(r'\$GNGGA', message):
            return 'GNGGA'

        return None

    def checkDataSum(self, message):
        payload = re.split(r'\*', message)
        return payload

    def parseGPGGA(self, message):
        parsed_input = message.split(',')
        self.time = parsed_input[1]  # UTC time
        self.lat = parsed_input[2]  # 纬度
        self.lat_ns = parsed_input[3]
        self.lon = parsed_input[4]
        self.lon_ew = parsed_input[5]
        self.fix = parsed_input[6]  # 0=未定位，1=非差分定位，2=差分定位，6=正在估算
        self.sats = parsed_input[7]  # 正在使用解算位置的卫星数量（00~12）（前面的0也将被传输）
        self.altitude = parsed_input[9]  # 海拔高度
        return self.current_values()

    def parseGNGGA(self, message):
        parsed_input = message.split(',')
        self.time = parsed_input[1]  # UTC time
        self.lat = parsed_input[2]
        self.lat_ns = parsed_input[3]
        self.lon = parsed_input[4]
        self.lon_ew = parsed_input[5]
        self.fix = parsed_input[6]
        self.sats = parsed_input[7]
        self.altitude = parsed_input[9]
        return self.current_values()

    def parseGPRMC(self, message):
        parsed_input = message.split(',')
        self.time = parsed_input[1]  # UTC time
        self.lat = parsed_input[3]
        self.lon = parsed_input[5]
        return self.current_values()

    def read(self):
        # '''
        # text = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
        # rawType = self.messageType(text)
        # if rawType is None:
        #     pass
        # elif rawType == 'GPGGA':
        #     return self.parseGPGGA(text)
        # elif rawType == 'GPRMC':
        #     return self.parseGPRMC(text)
        # '''

        while True:
            raw = self.GpsUart.readline()
            logging.info('gps++++++++++')
            logging.info(raw)  # $GPGGA,,,,,,0,00,99.99,,,,,,*48
            rawType = self.messageType(raw)

            if rawType is None:
                logging.info("rawType is None")
                pass
            elif rawType == 'GPGGA':
                logging.info("rawType == 'GPGGA'")
                return self.parseGPGGA(raw)
            elif rawType == 'GNGGA':
                logging.info("rawType == 'GNGGA'")
                return self.parseGNGGA(raw)
            # elif rawType == 'GPRMC':
            #  	return self.parseGPRMC(raw)

    def current_values(self):
        data = {}
        data['time'] = self.time
        data['lat'] = self.lat
        data['lat_ns'] = self.lat_ns
        data['lon'] = self.lon
        data['lon_ew'] = self.lon_ew
        data['fix'] = self.fix
        data['sats'] = self.sats
        data['altitude'] = self.altitude
        logging.info("current_values---:{}".format(data))
        return data


def gpsThreadStart(str1):
    launchGps = GpsParser()
    indexflag = 0
    while True:

        indexflag = indexflag + 1

        sendData = launchGps.read()
        logging.info("sendData:{}".format(sendData))
        global g_lastGPSData
        g_lastGPSData = sendData
        if indexflag % 6 == 0:
            sendData['checkId'] = did.macId
            try:
                pass
                # 发生gps经纬度请求给后台，返回解析后的实际街道地址
                # data = json.dumps(sendData)
                # inhttpRes = requests.post(config.sendGps, json=sendData)
                # print(inhttpRes)
                # logging.info('发送GPS请求后返回值:' + str(inhttpRes.text))
            except Exception as e:
                logging.info(e)
                logging.info('发送GPS请求出错')
            # print(sendData)
            indexflag = 0

        time.sleep(1)
