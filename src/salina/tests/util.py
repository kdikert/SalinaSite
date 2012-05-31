
from datetime import datetime, timedelta
import os
import numpy

import signaltests.util

from bedsenseweb.base import models
from bedsenseweb.tickets import models as ticketmodels

def create_test_data(signal_count):
    ts0 = 1269939960.0
    ts0 = 0.0
    t0 = datetime.fromtimestamp(ts0)
#    assert t0 == datetime(2010, 3, 30, 12, 06)
    
    person = models.MeasuredPerson.objects.create(nickname="John")
    device = models.Device.objects.create(identifier="FDAQ-test-device-1")
    service_provider = models.ServiceProvider.objects.create(name="Test service provider")
    installation = models.Installation.objects.create(name="Test installation", service_provider=service_provider, device=device)
    measurement_setup = models.MeasurementSetup.objects.create(installation=installation, measured_person=person, device=device, start_time=t0)
    
    assert models.ContinuousSignal.objects.all().count() == 0
    
    fragment_lists = []
    
    for signal_i in range(signal_count):
        signal_start_time = t0 + timedelta(hours=signal_i)
        
        test_signal_dict = signaltests.util.get_test_data('test_signal_clean_bcg_300s.npz')
        samplerate = 300.0
        dtype = numpy.dtype([("bcg_front", numpy.int32), ("bcg_back", numpy.int32)])
        data_length = len(test_signal_dict["bcg_front"])
        full_data_array = numpy.zeros(data_length, dtype=dtype)
        full_data_array["bcg_front"] = test_signal_dict["bcg_front"]
        full_data_array["bcg_back"] = test_signal_dict["bcg_back"]
        
        signal_fragment_length = int(samplerate * 15.0)
        signal_fragment_start_samples = range(0, data_length, signal_fragment_length)
        continuous_signal = measurement_setup.create_continuous_signal(signal_start_time, samplerate)
        fragments = []
        
        for i, signal_fragment_start_sample in enumerate(signal_fragment_start_samples):
            signal_fragment_chunk = full_data_array[signal_fragment_start_sample:signal_fragment_start_sample + signal_fragment_length]
            signal_fragment_start_time = signal_start_time + timedelta(seconds=signal_fragment_start_sample / samplerate)
            fragment = continuous_signal.append_data(signal_fragment_chunk, signal_fragment_start_time, i)
            fragments.append(fragment)
        
        continuous_signal.closed = True
        continuous_signal.save()
        
        assert all(os.path.exists(f.fragment_file_path) for f in fragments)
        # The relevant objects for the test
        continuous_signal.apply_analysis("NewIHRSleep")
        
        fragment_lists.append(fragments)
    
    return fragment_lists
