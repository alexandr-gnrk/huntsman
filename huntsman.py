import argparse


parser = argparse.ArgumentParser(
    description="Huntsman is a game that use steering behaviours.")
parser.add_argument(
    '-r', '--res',
    dest='res',
    type=int,
    nargs=2,
    metavar=('WIDTH', 'HEIGHT'),
    default=(900, 600),
    help='game window resolution')
parser.add_argument(
    '-ws', '--wsize',
    dest='wsize',
    type=int,
    nargs=2,
    metavar=('WIDTH', 'HEIGHT'),
    default=(1500, 1000),
    help='size of game world')
parser.add_argument(
    '-hr', '--hares',
    dest='hares',
    type=int,
    default=5,
    help='amount of hares')
parser.add_argument(
    '-wl', '--wolves',
    dest='wolves',
    type=int,
    default=2,
    help='amount of wolves')
parser.add_argument(
    '-df', '--deerflocks',
    dest='deerflocks',
    type=int,
    default=3,
    help='amount of deer families')
parser.add_argument(
    '-cs', '--camscale',
    dest='camscale',
    type=float,
    default=1.3,
    help='scale of camera inside game')


args = parser.parse_args()

import pygame
from game import View, Model

pygame.init()
screen = pygame.display.set_mode(args.res)
model = Model(
    args.wsize, 
    hares=args.hares, 
    wolves=args.wolves, 
    deer_families=args.deerflocks)

v = View(screen, model, args.camscale)
v.start()

