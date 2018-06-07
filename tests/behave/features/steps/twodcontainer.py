"""

    Autogenerated by ghenerate script, part of Quantarhei
    http://github.com/tmancal74/quantarhei
    Tomas Mancal, tmancal74@gmai.com

    Generated on: 2018-06-07 12:26:28

    Edit the functions below to give them desired functionality.
    In present version of `ghenerate`, no edits or replacements
    are perfomed in the feature file text.

"""

from behave import given
from behave import when
from behave import then

import quantarhei as qr

#
# Given ...
#
@given('that I have {N} TwoDSpectrum objects')
def step_given_1(context, N):
    """

        Given that I have {N} TwoDSpectrum objects

    """
    spectra = []
    ids = []
    
    for i_n in range(int(N)):
        spec = qr.TwoDSpectrum()
        itsid = id(spec)
        spectra.append(spec)
        ids.append(itsid)
        
    context.spectra = spectra
    context.ids = ids


#
# And ...
#
@given('I have an empty TwoDSpectrum container')
def step_given_2(context):
    """

        And I have an empty TwoDSpectrum container

    """
    container = qr.TwoDSpectrumContainer()
    context.container = container


#
# When ...
#
@when('I set the container to accept indexing by integers')
def step_when_3(context):
    """

        When I set the container to accept indexing by integers

    """
    cont = context.container
    
    cont.use_indexing_type("integer")


#
# And ...
#
@when('I add the spectra to the container one by one')
def step_when_4(context):
    """

        And I add the spectra to the container one by one

    """
    cont = context.container
    for spect in context.spectra:
        cont.set_spectrum(spect)


#
# Then ...
#
@then('TwoDSpectrum can be retrieved using the index {i}')
def step_then_5(context, i):
    """

        Then TwoDSpectrum can be retrieved using the index {i}

    """
    ids = context.ids
    cont = context.container
    
    length = len(ids)
    
    i_n = int(i)
    
    context.out_of_range = 0
    if i_n >= length:
        context.out_of_range = i_n
        return

    if not (ids[i_n] == id(cont.get_spectrum_by_index(i_n))):
        raise Exception("Incorrect retrieval of spectrum from container")


#
# But ...
#
@then('when index is out of bounds, I get an exception')
def step_then_6(context):
    """

        But when index is out of bounds, I get an exception

    """
    i_n = context.out_of_range
    if  i_n > 0:
        
        cont = context.container
        try:
            
            cont.get_spectrum_by_index(i_n)
            
        except KeyError as e:
            print(e, "'"+str(i_n)+"'")
            assert str(e) == "'"+str(i_n)+"'"
            
        except IndexError as e:
            print(e, "list index out of range")
            assert str(e) ==  "list index out of range"           
 
#
# And ...
#
@given('I have a ValueAxis of lenght {N} starting from zero with certain {step}')
def step_given_7(context, N, step):
    """

        And I have a ValueAxis of lenght {N} starting from zero with certain {step}

    """
    length = int(N)
    step = float(step)
    vaxis = qr.ValueAxis(0.0, length, step)
    
    context.vaxis = vaxis
    context.length = length
    context.step = step


#
# When ...
#
@when('I set the container to accept index by ValueAxis')
def step_when_8(context):
    """

        When I set the container to accept index by ValueAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    cont.use_indexing_type(vaxis)


#
# And ...
#
@when('I add the spectra to the container using values from ValueAxis')
def step_when_9(context):
    """

        And I add the spectra to the container using values from ValueAxis

    """
    cont = context.container
    spectra = context.spectra
    
    i_n = 0
    for val in context.vaxis.data:
        cont.set_spectrum(spectra[i_n], tag=val)
        i_n += 1
        


#
# Then ...
#
@then('TwoDSpectrum can be retrieved using values {val} from ValueAxis')
def step_then_10(context, val):
    """

        Then TwoDSpectrum can be retrieved using values {val} from ValueAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    context.out_of_range = 0
    
    vmax = vaxis.max
    
    if (float(val) < vmax):

        cont.get_spectrum(float(val))

    else:

        context.out_of_range=float(val)
        


#
# But ...
#
@then('when values are out of bounds, I get an exception')
def step_then_11(context):
    """

        But when values are out of bounds, I get an exception

    """
    val = context.out_of_range
    
    if val > 0:

        cont = context.container
        try:
            
            cont.get_spectrum(val)
            
        except Exception as e:
            assert str(e) == "Tag not compatible with the ValueAxis"        
        
#
# And ...
#
@given('I have a TimeAxis of lenght {N} starting from zero with certain {step}')
def step_given_12(context, N, step):
    """

        And I have a TimeAxis of lenght {N} starting from zero with certain {step}

    """
    length = int(N)
    step = float(step)
    vaxis = qr.TimeAxis(0.0, length, step)
    
    context.vaxis = vaxis
    context.length = length
    context.step = step

#
# When ...
#
@when('I set the container to accept index by TimeAxis')
def step_when_13(context):
    """

        When I set the container to accept index by TimeAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    cont.use_indexing_type(vaxis)


#
# And ...
#
@when('I add the spectra to the container using values from TimeAxis')
def step_when_14(context):
    """

        And I add the spectra to the container using values from TimeAxis

    """
    cont = context.container
    spectra = context.spectra
    
    i_n = 0
    for val in context.vaxis.data:
        cont.set_spectrum(spectra[i_n], tag=val)
        i_n += 1


#
# Then ...
#
@then('TwoDSpectrum can be retrieved using values {val} from TimeAxis')
def step_then_15(context, val):
    """

        Then TwoDSpectrum can be retrieved using values {val} from TimeAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    context.out_of_range = 0
    
    vmax = vaxis.max
    
    if (float(val) < vmax):

        cont.get_spectrum(float(val))

    else:

        context.out_of_range=float(val)

#
# And ...
#
@given('I have a FrequencyAxis of lenght {N} starting from zero with certain {step}')
def step_given_16(context, N, step):
    """

        And I have a FrequencyAxis of lenght {N} starting from zero with certain {step}

    """
    length = int(N)
    step = float(step)
    vaxis = qr.FrequencyAxis(0.0, length, step)
    
    context.vaxis = vaxis
    context.length = length
    context.step = step


#
# When ...
#
@when('I set the container to accept index by FrequencyAxis')
def step_when_17(context):
    """

        When I set the container to accept index by FrequencyAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    cont.use_indexing_type(vaxis)


#
# And ...
#
@when('I add the spectra to the container using values from FrequencyAxis')
def step_when_18(context):
    """

        And I add the spectra to the container using values from FrequencyAxis

    """
    cont = context.container
    spectra = context.spectra
    
    i_n = 0
    for val in context.vaxis.data:
        cont.set_spectrum(spectra[i_n], tag=val)
        i_n += 1


#
# Then ...
#
@then('TwoDSpectrum can be retrieved using values {val} from FrequencyAxis')
def step_then_19(context, val):
    """

        Then TwoDSpectrum can be retrieved using values {val} from FrequencyAxis

    """
    cont = context.container
    vaxis = context.vaxis
    
    context.out_of_range = 0
    
    vmax = vaxis.max
    
    if (float(val) < vmax):

        cont.get_spectrum(float(val))

    else:

        context.out_of_range=float(val)

#
# And ...
#
@given('I have a list of strings of lenght {N}')
def step_given_20(context, N):
    """

        And I have a list of strings of lenght {N}

    """
    strlist = []
    Nn = int(N)
    for k_n in range(Nn):
        strng = "string_"+str(k_n)
        strlist.append(strng)
        
    context.strlist = strlist


#
# When ...
#
@when('I set the container to accept index by strings')
def step_when_21(context):
    """

        When I set the container to accept index by strings

    """
    cont = context.container
    
    cont.use_indexing_type("string")


#
# And ...
#
@when('I add the spectra to the container using values from the list of strings')
def step_when_22(context):
    """

        And I add the spectra to the container using values from the list of strings

    """
    cont = context.container
    
    k_i = 0
    for strng in context.strlist:
        spect = context.spectra[k_i]
        cont.set_spectrum(spect, tag=strng)
        k_i += 1



#
# Then ...
#
@then('TwoDSpectrum can be retrieved using values from the list of strings')
def step_then_23(context):
    """

        Then TwoDSpectrum can be retrieved using values from the list of strings

    """
    
    cont = context.container
    
    for strng in context.strlist:
        
        cont.get_spectrum(strng)    


#
# But ...
#
@then('when values are not in the list of strings, I get an exception')
def step_then_24(context):
    """

        But when values are not in the list of strings, I get an exception

    """
    cont = context.container
    try:
        
        cont.get_spectrum("ahoj")
        
    except KeyError as e:
        assert str(e) == "'ahoj'"


###############################################################################
#
#  Fourier transform
#
###############################################################################
        

#
# Given ...
#
@given('that I have a TwoDSpectrumContainer containing {N} spectra indexed by ValueAxis')
def step_given_25(context, N):
    """

        Given that I have a TwoDSpectrumContainer containing {N} spectra indexed by ValueAxis

    """
    import numpy
    
    Nn = int(N)
    
    spectra = []
    
    def func(x,y,t):
        
        Delta = 10.0
        omega = 2.0*3.14159/20.0 
        gamma = 1.0/100.0
        
        data = numpy.zeros((len(x), len(y)))
        
        for i_x in range(len(x)):
                data[i_x, :] = numpy.exp(-((x[i_x]+y)/Delta)**2)* \
                                    numpy.cos(omega*t)*numpy.exp(-t/gamma)
        
        return data

    time = qr.TimeAxis(0.0, Nn, 2.0)
    xrange = qr.ValueAxis(-50.0, 100, 1.0).data
    yrange = qr.ValueAxis(-50.0, 100, 1.0).data
    
    cont = qr.TwoDSpectrumContainer()
    cont.use_indexing_type(time)
    
    for k_n in range(Nn):
        tt = time.data[k_n]
        data = func(xrange, yrange, tt)
        spect = qr.TwoDSpectrum()
        spect.set_data(data)
        spect.set_axis_1(xrange)
        spect.set_axis_3(yrange)
        spectra.append(spect)
        
        cont.set_spectrum(spect, tt)
        
    context.container = cont


#
# When ...
#
@when('I calculate Fourier transform on the container')
def step_when_26(context):
    """

        When I calculate Fourier transform on the container

    """
    cont = context.container

    cont.fft()


#
# Then ...
#
@then('I get correct pointwise Fourier transform of the spectra')
def step_then_27(context):
    """

        Then I get correct pointwise Fourier transform of the spectra

    """
    pass


#
# And ...
#
@then('the TwoDSpectrum container will be indexed by ValueAxis with frequencies corresponding to the original ValueAxis')
def step_then_28(context):
    """

        And the TwoDSpectrum container will be indexed by ValueAxis with frequencies corresponding to the original ValueAxis

    """
    pass

      