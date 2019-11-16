# coding=utf-8


def sqrt(x, low, high, deviation):
    mid = 0.5 * (low + high)
    if mid*mid - x < -deviation:
        print(mid, x, mid*mid - x)
        return sqrt(x, mid, high, deviation)
    elif mid*mid - x > deviation:
        print(mid, x, mid * mid - x)
        return sqrt(x, low, mid, deviation)
    else:
        print('get it: {}'.format(mid))
        return mid


if '__main__' == __name__:
    sqrt(100, 0, 100, 0.000001)