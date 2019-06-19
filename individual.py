# created by Sijmen van der Willik
# 2019-06-14 15:39

# boxes are [x1, y1, x2, y2]
import numpy as np
import cv2


class Box:
    def __init__(self, points, og_shape):
        # point should be shape (4,2), 4 points with (x, y)
        self.points = points
        self.shape = og_shape
        self.mask = None
        self.calc_mask()

    def calc_mask(self):
        mask = np.zeros(self.shape)
        coords = np.array(self.points)
        coords = coords.reshape((1, -1, 2))
        cv2.fillPoly(mask, coords, (1, 0, 0))
        self.mask = np.sum(mask, axis=2).astype(bool)
        return self.mask


class Individual:
    def __init__(self, img, grid_size):
        self.img = img
        self.canvas = np.zeros_like(img)
        self.im_shape = img.shape
        self.boxes = [["" for c in range(grid_size[1])] for r in range(grid_size[0])]
        self.grid_points = [["" for c in range(grid_size[1]-1)] for r in range(grid_size[0]-1)]
        self.grid_size = grid_size

        # grid size is (rows, columns)
        r_size = img.shape[0] // grid_size[0]
        c_size = img.shape[1] // grid_size[1]

        for c in range(grid_size[1] - 1):
            for r in range(grid_size[0] - 1):
                self.grid_points[r][c] = [(c+1) * c_size, (r+1) * r_size]

        for c in range(grid_size[1]):
            for r in range(grid_size[0]):
                x_min = c * c_size
                x_max = x_min + c_size
                y_min = r * r_size
                y_max = y_min + r_size

                try:
                    if r > 0 and c > 0:
                        tl = self.grid_points[r-1][c-1]
                    else:
                        tl = [x_min, y_min]
                except:
                    tl = [x_min, y_min]

                try:
                    if r > 0:
                        tr = self.grid_points[r-1][c]
                    else:
                        tr = [x_max, y_min]
                except:
                    tr = [x_max, y_min]

                try:
                    br = self.grid_points[r][c]
                except:
                    br = [x_max, y_max]

                try:
                    if c > 0:
                        bl = self.grid_points[r][c-1]
                    else:
                        bl = [x_min, y_max]
                except:
                    bl = [x_min, y_max]

                self.boxes[r][c] = Box([tl, tr, br, bl], self.im_shape)

    def error_shift(self, gpr, gpc, sx, sy):
        """Does a smaller, quicker error comparison

        :param gpr: grid point row
        :param gpc: grid point column
        :param sx: shift x
        :param sy: shift y
        :return:
        """
        # TODO create this function
        pass

    def mutate(self):
        for c in range(self.grid_size[1] - 1):
            for r in range(self.grid_size[0] - 1):
                err = self.get_error()
                shift_x = np.random.randint(-10, 10)
                shift_y = np.random.randint(-10, 10)

                # mutate grid points
                self.grid_points[r][c][0] += shift_x
                self.grid_points[r][c][1] += shift_y

                self.draw()
                new_err = self.get_error()

                if new_err > err:
                    self.grid_points[r][c][0] -= shift_x
                    self.grid_points[r][c][1] -= shift_y
                else:
                    print("OLD: {}, NEW: {} ({}/{})".format(err, new_err,
                                                            (self.grid_size[0] - 1) * c + r + 1,
                                                            (self.grid_size[1] - 1) * (self.grid_size[0] - 1)))

    def draw(self):
        self.canvas = np.zeros_like(self.img)
        for c in range(self.grid_size[1]):
            for r in range(self.grid_size[0]):
                mask = self.boxes[r][c].calc_mask()
                color = np.average(self.img[mask], axis=0)
                self.canvas[mask, :] = color.astype(np.uint)

    def get_error(self):
        err = np.sum((self.canvas.astype("float") - self.img.astype("float")) ** 2)
        return err
