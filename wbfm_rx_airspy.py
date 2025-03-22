#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Radio
# Author: danieltiganas
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip
import threading



class wbfm_rx_airspy(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Radio", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Radio")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "wbfm_rx_airspy")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.offset = offset = 200e3
        self.freq = freq = 101
        self.volume = volume = 1
        self.samp_rate = samp_rate = 2500000
        self.rf_gain = rf_gain = 28
        self.quadrature = quadrature = 250000
        self.mod = mod = 0
        self.freq_tune = freq_tune = freq*1e6+offset
        self.audio_rate = audio_rate = 48000

        ##################################################
        # Blocks
        ##################################################

        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'FFT Display')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'Band Display')
        self.top_layout.addWidget(self.tabs)
        self._volume_range = qtgui.Range(0, 10, 0.1, 1, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_layout_0.addWidget(self._volume_win)
        self._rf_gain_range = qtgui.Range(0, 45, 1, 28, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_layout_0.addWidget(self._rf_gain_win)
        self._mod_choices = {'Pressed': 1, 'Released': 0}

        _mod_toggle_button = qtgui.ToggleButton(self.set_mod, 'stereo/mono', self._mod_choices, False, 'value')
        _mod_toggle_button.setColors("default", "default", "default", "default")
        self.mod = _mod_toggle_button

        self.tabs_layout_0.addWidget(_mod_toggle_button)
        self._freq_range = qtgui.Range(80, 108, 0.1, 101, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_layout_0.addWidget(self._freq_win)
        self.soapy_custom_source_0 = None
        dev = 'driver=' + 'airspy'
        stream_args = ''
        tune_args = ['']
        settings = ['']
        self.soapy_custom_source_0 = soapy.source(dev, "fc32",
                                  1, 'bias-false',
                                  stream_args, tune_args, settings)
        self.soapy_custom_source_0.set_sample_rate(0, samp_rate)
        self.soapy_custom_source_0.set_bandwidth(0, 0)
        self.soapy_custom_source_0.set_antenna(0, 'RX')
        self.soapy_custom_source_0.set_frequency(0, freq_tune)
        self.soapy_custom_source_0.set_frequency_correction(0, 0)
        self.soapy_custom_source_0.set_gain_mode(0, False)
        self.soapy_custom_source_0.set_gain(0, rf_gain)
        self.soapy_custom_source_0.set_dc_offset_mode(0, False)
        self.soapy_custom_source_0.set_dc_offset(0, 0)
        self.soapy_custom_source_0.set_iq_balance(0, 0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=(int(audio_rate/1000)),
                decimation=(int(quadrature/1000)),
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=(int(audio_rate/1000)),
                decimation=(int(quadrature/1000)),
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=(int(audio_rate/1000)),
                decimation=(int(quadrature/1000)),
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            (freq*1e6+offset), #fc
            quadrature, #bw
            "", #name
            True, #plotfreq
            False, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.tabs_layout_1.addWidget(self._qtgui_sink_x_1_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            (freq*1e6), #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            False, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.tabs_layout_0.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (int(samp_rate/quadrature)),
            firdes.low_pass(
                1,
                samp_rate,
                60e3,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_selector_0_0_0 = blocks.selector(gr.sizeof_float*1,mod,0)
        self.blocks_selector_0_0_0.set_enabled(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,mod,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,mod)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_pll_0 = analog.wfm_rcv_pll(
        	demod_rate=quadrature,
        	audio_decimation=1,
        	deemph_tau=(50e-6),
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quadrature,
        	audio_decimation=1,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset, 1, 0, 0)
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=48000, tau=(50e-6))
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=48000, tau=(50e-6))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.analog_wfm_rcv_pll_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_wfm_rcv_pll_0, 1), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_selector_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_selector_0_0_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.analog_wfm_rcv_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.analog_wfm_rcv_pll_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_selector_0_0_0, 0), (self.audio_sink_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.soapy_custom_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "wbfm_rx_airspy")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.set_freq_tune(self.freq*1e6+self.offset)
        self.analog_sig_source_x_0.set_frequency(self.offset)
        self.qtgui_sink_x_1.set_frequency_range((self.freq*1e6+self.offset), self.quadrature)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_tune(self.freq*1e6+self.offset)
        self.qtgui_sink_x_0.set_frequency_range((self.freq*1e6), self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range((self.freq*1e6+self.offset), self.quadrature)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)
        self.blocks_multiply_const_vxx_0_0.set_k(self.volume)
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.volume)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 60e3, 1e3, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range((self.freq*1e6), self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.soapy_custom_source_0.set_gain(0, self.rf_gain)

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature
        self.qtgui_sink_x_1.set_frequency_range((self.freq*1e6+self.offset), self.quadrature)

    def get_mod(self):
        return self.mod

    def set_mod(self, mod):
        self.mod = mod
        self.blocks_selector_0.set_output_index(self.mod)
        self.blocks_selector_0_0.set_input_index(self.mod)
        self.blocks_selector_0_0_0.set_input_index(self.mod)

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.soapy_custom_source_0.set_frequency(0, self.freq_tune)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate




def main(top_block_cls=wbfm_rx_airspy, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
