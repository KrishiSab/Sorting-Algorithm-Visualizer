import pygame as pg
import pygame_widgets
import random
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
pg.init()


class Sorting:
    # color constants
    BLACK = 0, 0, 0
    YELLOW = 255, 255, 0
    LIGHT_GREY = (192, 192, 192)
    BACKGROUND_COLOR = LIGHT_GREY
    CURRENT_COLOR = YELLOW
    # Blues
    BAR_COLORS = [
        # (124, 232, 255),
        (85, 208, 255),
        (0, 172, 223),
        (0, 128, 191)
    ]
    # Greens
    CORRECT_COLORS = [
        (46, 182, 44),
        (87, 200, 77),
        (131, 212, 117)
    ]
    # white space constants
    SIDE_BUFFER = 100
    BOTTOM_BUFFER = 200
    # used for generating the randomized list
    MIN_POSSIBLE_VAL = 3
    MAX_POSSIBLE_VAL = 100
    # Fonts | see all available fonts via print(pg.font.get_fonts())
    COMIC_SANS = pg.font.SysFont("timesnewroman", 20)
    TITLE = pg.font.SysFont("ptserif", 19)
    TITLE.set_bold(True)
    LABEL = pg.font.SysFont("menlo", 15)
    # Slider settings
    s_x = 430
    s_y = 565
    s_width = 150
    s_height = 20
    s_min = 20
    s_max = 250
    s_step = 10
    s_initial = 100
    s_handleRadius = 10
    # TextBox settings
    t_width = 100
    t_height = s_height + 10
    t_x = s_x + s_width + 20
    t_y = s_y - 5
    t_border_thickness = 1
    # time complexity constants
    N = "O(N)"
    N2 = "O(N^2)"
    N_LOG_N = "O(N*log(N))"

    def __init__(self, size, n):
        # create surface + set caption
        self.size = self.width, self.height = size
        self.screen = pg.display.set_mode(self.size)
        title = "Sorting Algorithm Visualization"
        pg.display.set_caption(title)

        # set default to Bubble sort
        self.correct_elements = {}
        self.sorting_name = "Bubble Sort"
        self.best_time = self.N
        self.worst_time = self.N2
        self.average_time = self.N2
        # create slider
        self.slider = Slider(self.screen, self.s_x, self.s_y, self.s_width, self.s_height,
                             min=self.s_min, max=self.s_max, step=self.s_step,
                             initial=self.s_initial, handleRadius=self.s_handleRadius, colour=(220, 220, 220))
        # create textbox associated with slider
        self.label = TextBox(self.screen, self.t_x, self.t_y, self.t_width, self.t_height,
                             placeholdertext=str(self.s_initial), font=self.LABEL,
                             borderThickness=self.t_border_thickness)
        self.label.disable()  # allows TextBox to act as label
        # will be initialized in store_list_features()
        self.min_val = None
        self.max_val = None
        self.unit_bar_height = None
        self.unit_bar_width = None
        self.n = None
        self.start_x = None
        self.lst = None
        self.actual_side_buffer = None
        # create a new, randomized list
        self.create_new_list(n)

    def create_new_list(self, n, min_possible_val=MIN_POSSIBLE_VAL, max_possible_val=MAX_POSSIBLE_VAL):
        # generate new randomized list
        lst = []
        for null in range(n):
            val = random.randint(min_possible_val, max_possible_val)
            lst.append(val)

        # store list + list attributes
        self.lst = lst
        self.n = n
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.unit_bar_height = (self.height - self.BOTTOM_BUFFER) // self.max_val
        self.unit_bar_width = (self.width - self.SIDE_BUFFER) // len(lst)
        self.actual_side_buffer = self.width - (self.unit_bar_width * n)
        self.start_x = self.actual_side_buffer / 2

    def draw(self, index=None, sort=False):
        # if number in index list, it is a current element
        if index is None:
            index = []
        self.screen.fill(self.BACKGROUND_COLOR)
        self.slider.draw()
        self.label.draw()
        # draw current sort and time complexity
        title = self.TITLE.render(f"{self.sorting_name} | Size: {self.n} | Best: {self.best_time} | Average: "
                                  f"{self.average_time} | Worst: {self.worst_time}",
                                  True, self.BLACK)
        title_x = (self.width - title.get_width()) / 2
        self.screen.blit(title, (title_x, 430))
        # draw controls
        controls = self.COMIC_SANS.render("R - Reset | S - Sorted Reset | Space - Sort | Slider + R/S - "
                                          "Changes Array Size",
                                          True, self.BLACK)
        controls_x = (self.width - controls.get_width()) / 2
        self.screen.blit(controls, (controls_x, 480))
        # draw sorting header
        sorts = self.COMIC_SANS.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort",
                                       True, self.BLACK)
        sorts_x = (self.width - sorts.get_width()) / 2
        self.screen.blit(sorts, (sorts_x, 520))

        # draw list in bar format
        x = self.start_x
        if sort:
            self.lst.sort()
        for i in range(self.n):
            bar_color = self.BAR_COLORS[i % 3]
            if i in index:
                bar_color = self.CURRENT_COLOR
            if i in self.correct_elements:
                bar_color = self.correct_elements[i]

            val = self.lst[i]
            height = val * self.unit_bar_height
            width = self.unit_bar_width
            pg.draw.rect(self.screen, bar_color, (x, 0, width, height))
            x += width

        pg.display.update()

    def bubble_sort(self):
        for i in range(self.n - 1):
            swapped = False
            for j in range(self.n - 1 - i):
                if self.lst[j] > self.lst[j+1]:
                    swapped = True
                    self.lst[j], self.lst[j+1] = self.lst[j+1], self.lst[j]
                if j == self.n - 2 - i:
                    color = self.CORRECT_COLORS[(j+1) % 3]
                    self.correct_elements[j+1] = color
                self.draw([j+1])
                yield True

            if not swapped:
                index = 0
                while index < self.n:
                    color = self.CORRECT_COLORS[index % 3]
                    self.correct_elements[index] = color
                    index += 1
                self.draw()
                return

        color = self.CORRECT_COLORS[0]
        self.correct_elements[0] = color

    def insertion_sort(self):
        for i in range(self.n):
            if i == 0:
                self.draw([0])
                yield True
            elif self.lst[i] < self.lst[i-1]:
                while i > 0:
                    if self.lst[i] < self.lst[i-1]:
                        self.lst[i], self.lst[i-1] = self.lst[i-1], self.lst[i]
                        i -= 1
                        self.draw([i])
                    else:
                        break
                    yield True
                self.draw([i])
                yield True
            else:
                self.draw([i])
                yield True

        for ind in range(self.n):
            color = self.CORRECT_COLORS[ind % 3]
            self.correct_elements[ind] = color

        self.draw()
        return

    def merge_sort(self, begin, end):
        if end - begin > 1:
            mid = (end - begin) // 2 + begin
            self.draw([mid])
            yield True
            yield from self.merge_sort(begin, mid)
            yield from self.merge_sort(mid, end)

            left = []
            right = []

            left_iter = begin
            while left_iter < mid:
                left.append(self.lst[left_iter])
                left_iter += 1

            right_iter = mid
            while right_iter < end:
                right.append(self.lst[right_iter])
                right_iter += 1

            i = begin
            start_l = start_r = 0
            corresponding_r = mid

            while start_l < len(left) and start_r < len(right):
                if left[start_l] < right[start_r]:
                    self.lst[i] = left[start_l]
                    start_l += 1
                else:
                    self.lst[corresponding_r] = 0
                    self.lst[i] = right[start_r]
                    start_r += 1
                    corresponding_r += 1
                self.draw([i])
                yield True
                i += 1

            while start_l < len(left):
                self.lst[i] = left[start_l]
                start_l += 1
                self.draw([i])
                yield True
                i += 1

            while start_r < len(right):
                self.lst[corresponding_r] = 0
                self.lst[i] = right[start_r]
                start_r += 1
                corresponding_r += 1
                self.draw([i])
                yield True
                i += 1

            for x in range(begin, end):
                color = self.CORRECT_COLORS[x % 3]
                self.correct_elements[x] = color
            self.draw([i])
            yield True
        self.draw([begin])
        yield True

    def quick_sort(self, start, end):
        if start < end:
            self.draw()
            yield True

            piv = self.lst[end]
            ptr = start
            self.draw([end])
            yield True
            for i in range(start, end):
                self.draw([i, ptr])
                yield True
                if self.lst[i] <= piv:
                    self.lst[i], self.lst[ptr] = self.lst[ptr], self.lst[i]
                    self.draw([i, ptr])
                    yield True
                    ptr += 1

            self.draw([ptr, end])
            yield True
            self.lst[ptr], self.lst[end] = self.lst[end], self.lst[ptr]
            self.draw([ptr, end])
            yield True

            color = self.CORRECT_COLORS[ptr % 3]
            self.correct_elements[ptr] = color
            yield from self.quick_sort(start, ptr-1)
            yield from self.quick_sort(ptr+1, end)

        for x in range(start, end+1):
            color = self.CORRECT_COLORS[x % 3]
            self.correct_elements[x] = color
        self.draw([start])
        yield True


def main():
    # allows us to control sorting speed using tick method
    clock = pg.time.Clock()

    # CONSTANTS for initializing Sorting Visualizer
    screen_size = (850, 600)
    list_length = 100
    sorting_visualizer = Sorting(screen_size, list_length)

    # lets us know if we are sorting or not
    sorting = False

    # do we want to create a sorted list
    create_sorted = False

    # store attributes of curr sorting algo
    sorting_algo = sorting_visualizer.bubble_sort
    sorting_generator = None

    while True:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            if not create_sorted:
                sorting_visualizer.draw()
            else:
                sorting_visualizer.draw(sort=True)

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # read in user input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                elif event.key == pg.K_r:
                    create_sorted = False
                    sorting_visualizer.create_new_list(list_length)
                    sorting = False
                    sorting_visualizer.correct_elements.clear()
                elif event.key == pg.K_SPACE and not sorting:
                    sorting = True
                    if sorting_visualizer.sorting_name == "Merge Sort":
                        sorting_generator = sorting_algo(0, len(sorting_visualizer.lst))
                    elif sorting_visualizer.sorting_name == "Quick Sort":
                        sorting_generator = sorting_algo(0, len(sorting_visualizer.lst)-1)
                    else:
                        sorting_generator = sorting_algo()
                elif event.key == pg.K_b and not sorting:
                    sorting_algo = sorting_visualizer.bubble_sort
                    sorting_visualizer.sorting_name = "Bubble Sort"
                    sorting_visualizer.best_time = sorting_visualizer.N
                    sorting_visualizer.average_time = sorting_visualizer.N2
                    sorting_visualizer.worst_time = sorting_visualizer.N2
                elif event.key == pg.K_s:
                    sorting_visualizer.create_new_list(list_length)
                    create_sorted = True
                    sorting = False
                    sorting_visualizer.correct_elements.clear()
                elif event.key == pg.K_i and not sorting:
                    sorting_algo = sorting_visualizer.insertion_sort
                    sorting_visualizer.sorting_name = "Insertion Sort"
                    sorting_visualizer.best_time = sorting_visualizer.N
                    sorting_visualizer.average_time = sorting_visualizer.N2
                    sorting_visualizer.worst_time = sorting_visualizer.N2
                elif event.key == pg.K_m and not sorting:
                    sorting_algo = sorting_visualizer.merge_sort
                    sorting_visualizer.sorting_name = "Merge Sort"
                    sorting_visualizer.best_time = sorting_visualizer.N_LOG_N
                    sorting_visualizer.average_time = sorting_visualizer.N_LOG_N
                    sorting_visualizer.worst_time = sorting_visualizer.N_LOG_N
                elif event.key == pg.K_q and not sorting:
                    sorting_algo = sorting_visualizer.quick_sort
                    sorting_visualizer.sorting_name = "Quick Sort"
                    sorting_visualizer.best_time = sorting_visualizer.N_LOG_N
                    sorting_visualizer.average_time = sorting_visualizer.N_LOG_N
                    sorting_visualizer.worst_time = sorting_visualizer.N2
        # update slider value (copy elements from slider into textBox)
        list_length = sorting_visualizer.slider.getValue()
        sorting_visualizer.label.setText(f"Size: {list_length}")
        pygame_widgets.update(events)


if __name__ == "__main__":
    main()
