import numpy as np
from scipy.stats import linregress, t
from tqdm import tqdm
from utils import calculate_eigenvalues


def apply_t_test(slope1, slope2, std_err1, std_err2, dof1, dof2):
    slope_diff = slope1 - slope2
    std_err_diff = np.sqrt(std_err1**2 + std_err2**2)

    t_statistic = slope_diff / std_err_diff

    dof = dof1 + dof2

    p_value = 2 * t.cdf(-abs(t_statistic), dof)

    significance = p_value < 0.05

    the_slopes_are = 'different' if significance else 'equal'
    print(f"t-statistic: {t_statistic}")
    print(f"p-value: {p_value}")
    print(f"Significance: {significance}")
    print(f'The slopes are {the_slopes_are}.')



def check_slopes_are_different():

    area_sampling = np.linspace(1, 100, 20)
    shapes = ["square", "triangle"]

    combinations = [(shape, area) for area in area_sampling for shape in shapes]

    eigvalss = []
    for geometry_type, area in tqdm(combinations, desc="Test"):
        eigvals = calculate_eigenvalues(geometry_type, area)
        eigvalss.append(eigvals)

    slopes, std_errs, dofs = [], [], []
    for shape in shapes:
        shape_eigvalss = [
            eigvals
            for eigvals, (this_shape, _) in zip(eigvalss, combinations)
            if this_shape == shape
        ]
        shape_areas_tested = np.array(
            [area for this_shape, area in combinations if this_shape == shape]
        )
        shape_N_R_max = np.array(
            [len(eigvals) / np.max(eigvals) for eigvals in shape_eigvalss]
        )

        slope, intercept, r_value, p_value, std_err = linregress(
            shape_N_R_max, shape_areas_tested
        )
        slopes.append(slope)
        std_errs.append(std_err)
        dofs.append(len(shape_N_R_max) - 2)

    
    # for each pair of shapes, calculate the t-test
    for i in range(len(slopes)):
        for j in range(i+1, len(slopes)):
            print('Comparing slopes for shapes:', shapes[i], 'and', shapes[j])
            print('\n\n')
            print('Slope 1:', slopes[i])
            print('Slope 2:', slopes[j])
            print('Standard error 1:', std_errs[i])
            print('Standard error 2:', std_errs[j])
            apply_t_test(slopes[i], slopes[j], std_errs[i], std_errs[j], dofs[i], dofs[j])
            print('\n\n')


if __name__ == '__main__':
    check_slopes_are_different()
