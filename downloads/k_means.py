#! /usr/bin/env python

import pygame
import random
import math

# Window dimensions
width = 640
height = 400

k = 5
i = 1


def get_random_color():
    global i
    red = i % 2
    green = i/2 % 2
    blue = i/4 % 2
    i = i+1
    return red*255, green*255, blue*255


def diffuse_color((red, green, blue)):
    factor = 3
    add = (factor - 1) * 255 / factor
    red = red / factor + add
    green = green / factor + add
    blue = blue / factor + add
    return red, green, blue


def get_nearest_center(point, centers_dict):
    current_center = centers_dict.keys()[0]
    current_dist = distance(point, centers_dict[current_center])
    for center in centers_dict.keys():
        dist = distance(point, centers_dict[center])
        if dist < current_dist:
            current_center = center
            current_dist = dist
    return current_center


def main():
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True

    base_points = get_base_points(width - 1, height - 1, n=500, nclouds=20)
    initial_centers = get_random_points(width - 1, height - 1, n=6)
    centers = {str(p): p for p in initial_centers}
    colors = {str(p): get_random_color() for p in initial_centers}

    while running:
        point_groups = {center: [] for center in centers}

        for point in centers:
            draw_point(screen, centers[point], colors[point])

        for point in base_points:
            current_center = get_nearest_center(point, centers)
            color = diffuse_color(colors[current_center])
            draw_point(screen, point, color)
            point_groups[current_center].append(point)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(4)
        screen.fill((0, 0, 0))

        for center in point_groups:
            points = point_groups[center]
            if not points:
                initial_centers = get_random_points(width - 1, height - 1, n=3)
                centers = {str(p): p for p in initial_centers}
                colors = {str(p): get_random_color() for p in initial_centers}
                break
            new_center_location = points_average(points)
            centers[center] = new_center_location


def draw_point(screen, (x, y), color):
    for dx in range(-5, 5):
        for dy in range(-5, 5):
            screen.set_at((x + dx, y + dy), color)


def get_random_points(max_x, max_y, n=100, min_x=0, min_y=0):
    res = []
    for i in range(n):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        point = x, y
        res.append(point)
    return res


def get_base_points(max_x, max_y, n=100, nclouds=5):
    result = []
    cloud_size = n / nclouds
    for i in range(nclouds):
        cloud_x = random.randint(0, max_x)
        cloud_y = random.randint(0, max_y)
        size = 50
        points = get_random_points(cloud_x+size, cloud_y+size, n=cloud_size, min_x=cloud_x-size, min_y=cloud_y-size)
        result.extend(points)
    return result


def distance((x1, y1), (x2, y2)):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def points_average(points):
    x = y = n = 0
    for x1, y1 in points:
        x += x1
        y += y1
        n += 1
    return (x/n, y/n)

main()
