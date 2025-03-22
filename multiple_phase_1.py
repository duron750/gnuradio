#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Multiple Cariers
# Author: dan
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import math



from gnuradio import qtgui

class multiple_phase_1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Multiple Cariers", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Multiple Cariers")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "multiple_phase_1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.outbuffer = outbuffer = 100
        self.freq_offset = freq_offset = 250e3
        self.fm_max_dev = fm_max_dev = 50e3
        self.audio_samp_rate = audio_samp_rate = 380e3

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            audio_samp_rate*12, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.blocks_vco_f_0 = blocks.vco_f(audio_samp_rate, 753982.2369, 1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0 = filter.fir_filter_fcc(
            1,
            firdes.complex_band_pass(
                1,
                audio_samp_rate,
                0,
                140000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_1_0 = analog.sig_source_f(audio_samp_rate, analog.GR_COS_WAVE, 40e3, 1, 0, 0)
        self.analog_sig_source_x_1 = analog.sig_source_f(audio_samp_rate, analog.GR_COS_WAVE, 20e3, 1, 0, 0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, 3e3, 0.4, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, 2e3, 0.3, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, 1000, 0.3, 0, 0)
        self.analog_fm_preemph_0_1 = analog.fm_preemph(fs=audio_samp_rate, tau=50e-6, fh=-1.0)
        self.analog_fm_preemph_0_0 = analog.fm_preemph(fs=audio_samp_rate, tau=50e-6, fh=-1.0)
        self.analog_fm_preemph_0 = analog.fm_preemph(fs=audio_samp_rate, tau=50e-6, fh=-1.0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_preemph_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_fm_preemph_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_fm_preemph_0_1, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.analog_sig_source_x_0, 0), (self.analog_fm_preemph_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.analog_fm_preemph_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.analog_fm_preemph_0_1, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_vco_f_0, 0), (self.band_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "multiple_phase_1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_outbuffer(self):
        return self.outbuffer

    def set_outbuffer(self, outbuffer):
        self.outbuffer = outbuffer

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_fm_max_dev(self):
        return self.fm_max_dev

    def set_fm_max_dev(self, fm_max_dev):
        self.fm_max_dev = fm_max_dev

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_1_0.set_sampling_freq(self.audio_samp_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_samp_rate, 0, 140000, 2000, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.audio_samp_rate*12)




def main(top_block_cls=multiple_phase_1, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

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
