import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.widgets import CheckButtons
# The parametrized function to be plotted
from knn import learn_all_knn, WeightType
from loo import loo
from parsen_window import P, learn_all_parsen, T, E, Q, G
from standard import standard_method
from util import generate_all_points, generate_klasses, set_learn_data, accuracy

LEARN_MODE = 'П(r)'
KNN_MODE = WeightType.NONE

X1_BORDERS = [1, 2, 3]
X2_BORDERS = [1, 2, 3]

x1_min = min(X1_BORDERS)
x1_max = max(X1_BORDERS)
x2_min = min(X2_BORDERS)
x2_max = max(X2_BORDERS)

KLASSES = generate_klasses(X1_BORDERS, X2_BORDERS)
init_learn_number = 60
init_test_number = 60
H = 4
STANDARD_PERCENTAGE = 50
K = 5
points = generate_all_points(init_learn_number, x1_min, x1_max, x2_min, x2_max)
points_dict = set_learn_data(points, KLASSES)
points_for_test = generate_all_points(init_test_number, x1_min, x1_max, x2_min, x2_max)
# Define initial parameters


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
# line, = plt.plot(t, f(t, init_amplitude, init_frequency), lw=2)
print(points_dict)
print(standard_method(STANDARD_PERCENTAGE, points_dict, KLASSES))
dots, = plt.plot(list(map(lambda v: v.x, points)), list(map(lambda v: v.y, points)), 'ok')
standards, = plt.plot(list(map(lambda v: v.x, standard_method(STANDARD_PERCENTAGE, points_dict, KLASSES))),
                      list(map(lambda v: v.y, standard_method(STANDARD_PERCENTAGE, points_dict, KLASSES))),
                      'or')  # s=sizes

ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_xlim([x1_min - 0.5, x1_max + 0.5])
ax.set_ylim([x2_min - 0.5, x2_max + 0.5])
for x1 in X1_BORDERS:
    plt.plot([x1, x1], [x2_min, x2_max], color="black")
# draw x2_boundaries
for x2 in X2_BORDERS:
    plt.plot([x1_min, x1_max], [x2, x2], color="black")
axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.2, bottom=0.4)

# Make a horizontal slider to control the quantity.
axnumlearn = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
learn_points_num_slider = Slider(
    valstep=5,
    ax=axnumlearn,
    label='learn num',
    valmin=10,
    valmax=400,
    valinit=init_learn_number,
)

axnum = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
points_num_slider = Slider(
    valstep=5,
    ax=axnum,
    label='quantity test',
    valmin=10,
    valmax=400,
    valinit=init_test_number,
)

axh = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
h_slider = Slider(
    valstep=0.1,
    ax=axh,
    label='h',
    valmin=0.2,
    valmax=3,
    valinit=H,
)

axpercent = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
percent_slider = Slider(
    valstep=0.5,
    ax=axpercent,
    label='%',
    valmin=1,
    valmax=100,
    valinit=STANDARD_PERCENTAGE,
)

axk = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
k_slider = Slider(
    valstep=0.5,
    ax=axk,
    label='k',
    valmin=1,
    valmax=len(points),
    valinit=3,
)

rax = plt.axes([0.05, 0.7, 0.1, 0.15], facecolor=axcolor)
alg_mod_radio = RadioButtons(rax, ('П(r)', 'T(r)', 'E(r)', 'Q(r)', 'G(r)', 'KNN'))

rax1 = plt.axes([0.05, 0.4, 0.1, 0.15], facecolor=axcolor)
knn_mode_radio = RadioButtons(rax1, ('None', 'Linear', 'Exp'))


def update(val):
    global points
    global points_dict
    global points_for_test
    global init_learn_number
    global init_test_number
    init_learn_number = learn_points_num_slider.val
    init_test_number = points_num_slider.val
    points = generate_all_points(init_learn_number, x1_min, x1_max, x2_min, x2_max)

    points_dict = set_learn_data(points, KLASSES)
    points_for_test = generate_all_points(init_test_number, x1_min, x1_max, x2_min, x2_max)

    x = list(map(lambda v: v.x, points))
    y = list(map(lambda v: v.y, points))
    dots.set_xdata(x)
    dots.set_ydata(y)

    standard = standard_method(STANDARD_PERCENTAGE, points_dict, KLASSES)
    x = list(map(lambda v: v.x, standard))
    y = list(map(lambda v: v.y, standard))
    standards.set_xdata(x)
    standards.set_ydata(y)
    fig.canvas.draw_idle()


def update_modes(val):
    global H
    global K
    global STANDARD_PERCENTAGE
    H = h_slider.val
    K = int(k_slider.val)
    STANDARD_PERCENTAGE = percent_slider.val

    standard = standard_method(STANDARD_PERCENTAGE, points_dict, KLASSES)
    x = list(map(lambda v: v.x, standard))
    y = list(map(lambda v: v.y, standard))
    standards.set_xdata(x)
    standards.set_ydata(y)


def calculate(event):
    if alg_mod_radio.value_selected == 'П(r)':
        solved = learn_all_parsen(points_for_test, H, points_dict, lambda x: P(x), True, k=None)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: P(x), mode=None, is_fixed=True)
        print("Вікно Парзена: П(r) фіксованої довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))

        solved = learn_all_parsen(points_for_test, None, points_dict, lambda x: P(x), False, k=K)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: P(x), mode=None, is_fixed=False)
        print("Вікно Парзена: П(r) динамічної довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    elif alg_mod_radio.value_selected == 'T(r)':
        solved = learn_all_parsen(points_for_test, H, points_dict, lambda x: T(x), True, k=None)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: T(x), mode=None, is_fixed=True)
        print("Вікно Парзена: T(r) фіксованої довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))

        solved = learn_all_parsen(points_for_test, None, points_dict, lambda x: T(x), False, k=K)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: T(x), mode=None, is_fixed=False)
        print("Вікно Парзена: T(r) динамічної довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    elif alg_mod_radio.value_selected == 'E(r)':
        solved = learn_all_parsen(points_for_test, H, points_dict, lambda x: E(x), True, k=None)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: E(x), mode=None,  is_fixed=True)
        print("Вікно Парзена: E(r) фіксованої довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))

        solved = learn_all_parsen(points_for_test, None, points_dict, lambda x: E(x), is_fixed=False, k=K, )
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: E(x), mode=None, is_fixed=False)
        print("Вікно Парзена: E(r) динамічної довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    elif alg_mod_radio.value_selected == 'Q(r)':
        solved = learn_all_parsen(points_for_test, H, points_dict, lambda x: Q(x), True, k=None)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: Q(x), mode=None,  is_fixed=True)
        print("Вікно Парзена: Q(r) фіксованої довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))

        solved = learn_all_parsen(points_for_test, None, points_dict, lambda x: Q(x), False, k=K)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: Q(x), mode=None, is_fixed=False)
        print("Вікно Парзена: Q(r) динамічної довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    elif alg_mod_radio.value_selected == 'G(r)':
        solved = learn_all_parsen(points_for_test, H, points_dict, lambda x: G(x), True, k=None)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: G(x), mode=None,  is_fixed=True)
        print("Вікно Парзена: G(r) фіксованої довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))

        solved = learn_all_parsen(points_for_test, None, points_dict, lambda x: G(x), is_fixed=False, k=K)
        loo_val = loo(points_dict, H, K, STANDARD_PERCENTAGE, KLASSES, False, lambda x: G(x), mode=None, is_fixed=False)
        print("Вікно Парзена: G(r) динамічної довжини")
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    elif alg_mod_radio.value_selected == 'KNN':
        solved = learn_all_knn(points_for_test, points_dict, K, KNN_MODE)
        loo_val = loo(data_set=points_dict, h=None, k=K, percentage=STANDARD_PERCENTAGE,
                      klasses=KLASSES,
                      is_knn=True, mode=KNN_MODE, kernel=None, is_fixed= False)
        print("knn: k =", K, ", mode =" ,  KNN_MODE)
        print("accuracy: %s/%s" % (accuracy(solved, KLASSES), len(solved)))
        print("loo: %s/%s" % (loo_val, len(points_dict)))
    print("---------------------------")


# register the update function with each slider
learn_points_num_slider.on_changed(update)
points_num_slider.on_changed(update)
h_slider.on_changed(update_modes)
k_slider.on_changed(update_modes)

percent_slider.on_changed(update_modes)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
calcax = plt.axes([0.8, 0, 0.1, 0.04])
button = Button(calcax, 'calculate', color=axcolor, hovercolor='0.975')

button.on_clicked(calculate)


def alg_mod(label):
    if label == "KNN":
        rax1.set_visible(True)
    else:
        rax1.set_visible(False)


alg_mod_radio.on_clicked(alg_mod)


def knn_mode(label):
    global KNN_MODE
    if label == "None":
        KNN_MODE = WeightType.NONE
    elif label == "Linear":
        KNN_MODE = WeightType.LINEAR
    elif label == "Exp":
        KNN_MODE = WeightType.EXP

knn_mode_radio.on_clicked(knn_mode)

plt.show()
