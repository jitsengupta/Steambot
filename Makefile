# Define the cross-compiler
MPYCROSS = mpy-cross

# 
# In the following, name things in their order of requirement, to
# avoid having to specify explicit dependency.
LIBOBJS = Net.mpy Sensors.mpy Lights.mpy Buzzer.mpy Counters.mpy Log.mpy StateModel.mpy Motors.mpy
# Define app objects that you want precompiled - all except main and boot
# recommended
APPOBJS = Movement.mpy

%.mpy: %.py
	$(MPYCROSS) $<

all: $(LIBOBJS) $(APPOBJS)

clean:
	rm -f $(LIBOBJS) $(APPOBJS)
