#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: SSB Receiver V0.6
# Author: OZ9AEC
# Description: Simple SSB receiver prototype (LFRX)
# Generated: Wed Oct 10 09:54:58 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class ssb_rx_v06_LF(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="SSB Receiver V0.6")

        ##################################################
        # Variables
        ##################################################
        self.width = width = 2600
        self.lo_offset = lo_offset = 200e6
        self.freq = freq = 7.1e6
        self.center = center = -1500
        self.volume = volume = -10
        self.trans = trans = 300
        self.samp_rate = samp_rate = 10e6
        self.offset_fine = offset_fine = 0
        self.offset_coarse = offset_coarse = 0
        self.mix_gain = mix_gain = 8
        self.low = low = center-width/2
        self.high = high = center+width/2
        self.gain = gain = 7
        self.freq_tune = freq_tune = freq + lo_offset
        self.audio_rate = audio_rate = 50e3
        self.agc_decay = agc_decay = 50e-6
        self.LO = LO = 0

        ##################################################
        # Blocks
        ##################################################
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='Volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=-30,
        	maximum=0,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_volume_sizer, 4, 1, 1, 1)
        _trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._trans_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	label='Trans',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._trans_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	minimum=100,
        	maximum=2000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_trans_sizer, 3, 1, 1, 1)
        _offset_fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_fine_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	label='Offset (fine)',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_fine_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	minimum=-1000,
        	maximum=1000,
        	num_steps=400,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_fine_sizer, 2, 1, 1, 1)
        _offset_coarse_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_coarse_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	label='Offset (coarse)',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_coarse_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	minimum=-100000,
        	maximum=100000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_coarse_sizer, 2, 2, 1, 1)
        self.nbook = self.nbook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "RF Spectrum")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "IF Spectrum")
        self.GridAdd(self.nbook, 0, 0, 1, 3)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='RF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_gain_sizer, 4, 0, 1, 1)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=3.5e6,
        	maximum=14.5e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 1, 0, 1, 3)
        self._agc_decay_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.agc_decay,
        	callback=self.set_agc_decay,
        	label='AGC',
        	choices=[100e-6, 50e-6, 10e-6],
        	labels=['Fast', 'Medium', 'Slow'],
        )
        self.GridAdd(self._agc_decay_chooser, 3, 2, 1, 1)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='dB',
        	minval=-100,
        	maxval=-10,
        	factor=1.0,
        	decimal_places=1,
        	ref_level=0,
        	sample_rate=audio_rate,
        	number_rate=15,
        	average=True,
        	avg_alpha=0.1,
        	label='S-Meter',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.GridAdd(self.wxgui_numbersink2_0.win, 5, 1, 1, 2)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.nbook.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='IF Spectrum',
        	peak_hold=False,
        )
        self.nbook.GetPage(1).Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.nbook.GetPage(0).GetWin(),
        	baseband_freq=freq+LO,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=768,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='RF Spectrum',
        	peak_hold=False,
        )
        self.nbook.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        _width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._width_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	label='Width',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._width_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	minimum=100,
        	maximum=5000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_width_sizer, 2, 0, 1, 1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl-0' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq_tune, 0)
        self.rtlsdr_source_0.set_freq_corr(-65, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        _mix_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._mix_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_mix_gain_sizer,
        	value=self.mix_gain,
        	callback=self.set_mix_gain,
        	label='Mix Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._mix_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_mix_gain_sizer,
        	value=self.mix_gain,
        	callback=self.set_mix_gain,
        	minimum=0,
        	maximum=49.6,
        	num_steps=124,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_mix_gain_sizer, 4, 2, 1, 1)
        self._lo_offset_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.lo_offset,
        	callback=self.set_lo_offset,
        	label='Upconverter LO',
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._lo_offset_text_box, 5, 0, 1, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(int(samp_rate/audio_rate), (firdes.low_pass(1, audio_rate, 25000, 2000, firdes.WIN_HAMMING, 6.76)), -(offset_coarse+offset_fine), samp_rate)
        _center_sizer = wx.BoxSizer(wx.VERTICAL)
        self._center_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	label='Center',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._center_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	minimum=-5000,
        	maximum=5000,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_center_sizer, 3, 0, 1, 1)
        self.blocks_rms_xx_0 = blocks.rms_cf(0.0001)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(20, 1, -5)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10**(1.*(volume+15)/10), ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, audio_rate, low, high, trans, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_agc2_xx_0 = analog.agc2_cc(0.1, agc_decay, 0.3, 1.0)
        self.analog_agc2_xx_0.set_max_gain(2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.blocks_rms_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_nlog10_ff_0, 0), (self.wxgui_numbersink2_0, 0))    
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_nlog10_ff_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_fftsink2_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))    

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._width_slider.set_value(self.width)
        self._width_text_box.set_value(self.width)

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self.set_freq_tune(self.freq + self.lo_offset)
        self._lo_offset_text_box.set_value(self.lo_offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_tune(self.freq + self.lo_offset)
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq+self.LO)

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._center_slider.set_value(self.center)
        self._center_text_box.set_value(self.center)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self.blocks_multiply_const_vxx_0.set_k((10**(1.*(self.volume+15)/10), ))

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self._trans_slider.set_value(self.trans)
        self._trans_text_box.set_value(self.trans)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_offset_fine(self):
        return self.offset_fine

    def set_offset_fine(self, offset_fine):
        self.offset_fine = offset_fine
        self._offset_fine_slider.set_value(self.offset_fine)
        self._offset_fine_text_box.set_value(self.offset_fine)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_offset_coarse(self):
        return self.offset_coarse

    def set_offset_coarse(self, offset_coarse):
        self.offset_coarse = offset_coarse
        self._offset_coarse_slider.set_value(self.offset_coarse)
        self._offset_coarse_text_box.set_value(self.offset_coarse)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_mix_gain(self):
        return self.mix_gain

    def set_mix_gain(self, mix_gain):
        self.mix_gain = mix_gain
        self._mix_gain_slider.set_value(self.mix_gain)
        self._mix_gain_text_box.set_value(self.mix_gain)

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_high(self):
        return self.high

    def set_high(self, high):
        self.high = high
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.rtlsdr_source_0.set_gain(self.gain, 0)

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.rtlsdr_source_0.set_center_freq(self.freq_tune, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.wxgui_fftsink2_0_0.set_sample_rate(self.audio_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.audio_rate, 25000, 2000, firdes.WIN_HAMMING, 6.76)))
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, self.low, self.high, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_agc_decay(self):
        return self.agc_decay

    def set_agc_decay(self, agc_decay):
        self.agc_decay = agc_decay
        self._agc_decay_chooser.set_value(self.agc_decay)
        self.analog_agc2_xx_0.set_decay_rate(self.agc_decay)

    def get_LO(self):
        return self.LO

    def set_LO(self, LO):
        self.LO = LO
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq+self.LO)


def main(top_block_cls=ssb_rx_v06_LF, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
