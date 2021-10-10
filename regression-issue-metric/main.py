import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.widgets import CheckButtons

from kelner import P, T, E, Q, G
from nadarayawatsonmodel import *

from utils import get_training_data, get_testing_data, function

LEARN_MODE = 'П(r)'

N = 60
H = 1
K = 5
fig, ax = plt.subplots()
data_to_draw = np.arange(-2, 2, 0.01)
training_data = get_training_data(N)
test_data = get_testing_data(N)
# dots, = plt.plot(list(map(lambda v: v.x, points)), list(map(lambda v: v.y, points)), 'ok')
plt.plot(data_to_draw, function(data_to_draw), label='original')
training_dots, = plt.plot(training_data, list(map(function_with_mistakes, training_data)), "ok", markersize=2)
model, = plt.plot([0.5], [0.5], "r")

ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_xlim([-2.1, 2.1])
ax.set_ylim([-0.5, 1.5])

axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.35)

# Make a horizontal slider to control the quantity.
axnum = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
points_num_slider = Slider(
    valstep=5,
    ax=axnum,
    label='quantity',
    valmin=10,
    valmax=400,
    valinit=N,
)

axh = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
h_slider = Slider(
    valstep=0.05,
    ax=axh,
    label='h',
    valmin=0.05,
    valmax=1,
    valinit=H,
)

axk = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
k_slider = Slider(
    valstep=1,
    ax=axk,
    label='k',
    valmin=3,
    valmax=20,
    valinit=K,
)

rax = plt.axes([0.05, 0.7, 0.1, 0.2], facecolor=axcolor)
alg_mod_radio = RadioButtons(rax, ('П(r)', 'T(r)', 'E(r)', 'Q(r)', 'G(r)'))

rax1 = plt.axes([0.05, 0.3, 0.1, 0.2], facecolor=axcolor)
mod_radio = RadioButtons(rax1, ('fixed', 'chngd'))


def update(val):
    global N
    global training_data
    global test_data
    N = val
    training_data = get_training_data(N)
    test_data = get_testing_data(N)
    reset_mistaken_data()
    training_dots.set_xdata(training_data)
    training_dots.set_ydata(list(map(function_with_mistakes, training_data)))
    model.set_xdata([])
    model.set_ydata([])
    fig.canvas.draw_idle()


def update_modes(val):
    global H
    global K
    H = h_slider.val
    K = k_slider.val
    fig.canvas.draw_idle()


def normalize(data):
    normalized = list()
    xs = data.copy()
    for x in xs:
        xs_copy = xs.copy()
        xs_copy.remove(x)
        model1 = NadarayaWatsonModel(xs_copy, function_with_mistakes, 0.6, lambda r: G(r), Mode.FIXED, k=0)
        # print(x, model1.calculate(x) / function_with_mistakes(x))
        if function_with_mistakes(x) / model1.calculate(x) < 5:
            print(model1.calculate(x) / function_with_mistakes(x))
            normalized.append(x)
    return normalized


def loess(event):
    global training_data
    global test_data

    training_data = normalize(training_data)
    test_data = normalize(test_data)
    training_dots.set_xdata(training_data)
    training_dots.set_ydata(list(map(function_with_mistakes, training_data)))
    fig.canvas.draw_idle()


def calculate(event):
    solver = None
    if mod_radio.value_selected == 'fixed':
        if alg_mod_radio.value_selected == 'П(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: P(r),
                                         Mode.FIXED)
            print("П(r) фіксованої довжини:")
        elif alg_mod_radio.value_selected == 'T(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: T(r),
                                         Mode.FIXED)
            print("T(r) фіксованої довжини:")
        elif alg_mod_radio.value_selected == 'E(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: E(r),
                                         Mode.FIXED)
            print("E(r) фіксованої довжини:")
        elif alg_mod_radio.value_selected == 'Q(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: Q(r),
                                         Mode.FIXED)
            print("Q(r) фіксованої довжини:")
        elif alg_mod_radio.value_selected == 'G(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: G(r),
                                         Mode.FIXED)
            print("G(r) фіксованої довжини:")

    elif mod_radio.value_selected == 'chngd':
        if alg_mod_radio.value_selected == 'П(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: P(r),
                                         Mode.CHANGING, K)
            print("П(r) динамічної довжини:")
        elif alg_mod_radio.value_selected == 'T(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: T(r),
                                         Mode.CHANGING, K)
            print("T(r) динамічної довжини:")
        elif alg_mod_radio.value_selected == 'E(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: E(r),
                                         Mode.CHANGING, K)
            print("E(r) динамічної довжини:")
        elif alg_mod_radio.value_selected == 'Q(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: Q(r),
                                         Mode.CHANGING, K)
            print("Q(r) динамічної довжини:")
        elif alg_mod_radio.value_selected == 'G(r)':
            solver = NadarayaWatsonModel(training_data, lambda x: function_with_mistakes(x), H, lambda r: G(r),
                                         Mode.CHANGING, K)
            print("G(r) динамічної довжини:")

    print("Q:", solver.empirical_risk(test_data))
    model.set_xdata(data_to_draw)
    model.set_ydata(solver.calculate_all(data_to_draw))
    fig.canvas.draw_idle()

    print("---------------------------")


# register the update function with each slider
points_num_slider.on_changed(update)
h_slider.on_changed(update_modes)
k_slider.on_changed(update_modes)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
calcax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(calcax, 'calculate', color=axcolor, hovercolor='0.975')

calcax1 = plt.axes([0.6, 0.025, 0.1, 0.04])
button1 = Button(calcax1, 'smooth', color=axcolor, hovercolor='0.975')

button.on_clicked(calculate)
button1.on_clicked(loess)

plt.show()
