from brian2 import *

# Neurons = 2
# tau_m = 10 * ms
# reset_pot = 0 * mV
# thresh = 15 * mV
# In_cur = 20 * mV

# model_eqs = '''
# dv/dt = (-v + I)/tau_m : volt
# I : volt
# '''

# start_scope()
# network = NeuronGroup(Neurons, model=model_eqs, threshold='v>thresh',reset='v=reset_pot')
# network.v = reset_pot
# network.I = In_cur

# spikes = SpikeMonitor(network)
# trace_v = StateMonitor(network, ['v'], record=True)

# run(0.1*second)
# figure(1)
# plot(trace_v.t/ms, trace_v[0].v/mV)
# xlabel('Time (ms)', fontsize=24)
# ylabel('v (mV)', fontsize=24)
# yticks([0,4,8,12,16])
# show()

# refract_delta = 5
# tau_mem = 10
# v_th = 15
# Is = linspace(0,50,51)

# f1 = 1.0 / (tau_mem * log(Is / (Is - v_th)))
# f2 = 1.0 / (refract_delta + tau_mem * log(Is / (Is - v_th)))

# figure(2)
# plot(Is, f1, 'k-')
# plot(Is, f2, 'k--')
# plot([20, 20], [0, 0.3], 'r-')
# xlabel('I', fontsize=24)
# ylabel('f (kHz)', fontsize=24)
# yticks([0, .1, .2, .3])
# show()

start_scope()
v_rest = 0*mV
v_thr = 10*mV
tau_m = 10*ms

eqs = '''
dv/dt = -(v-v_rest-I)/tau_m : volt (unless refractory)
I : volt
'''

In = NeuronGroup(1, model=eqs, threshold='v>v_thr',reset='v=v_rest', refractory=5*ms)
In.v = [5*mV]
In.I = [20*mV]

Hidd = NeuronGroup(1, model=eqs, threshold='v>v_thr', reset='v=v_rest', refractory=0*ms)
Hidd.v = [0*mV]
Hidd.I = [0*mV]

S = Synapses(In, Hidd, on_pre='v_post+=10*mV')
S.connect(i=In, j=Hidd)

trace_In = StateMonitor(In, 'v', record=True)
trace_Hidd = StateMonitor(Hidd, 'v', record=True)

run(50*ms)

figure(1)
plot(trace_In.t/ms, trace_In.v[0], '-b', label='Input Neuron')
plot(trace_Hidd.t/ms, trace_Hidd.v[0], '-g', lw=2, label='Hidden Neuron')
xlabel('Time (ms)')
ylabel('v')
show()