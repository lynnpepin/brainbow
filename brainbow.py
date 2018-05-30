import argparse
from bbworld import save_pic, load_pic, iterate_board

def _save_iteration(savename, save_board, iteration, max_iterations):
    if (savename):
        filename = savename[0]
        num_digits = len(str(max_iterations))
        filename += "_" + str(iteration).zfill(num_digits) + ".png"
        save_pic(save_board, filename)


def run(loadname, iterations, savename):
    #main(args.loadpic, args.iterate, args.print, args.printonce, ags.savepic)
    board = load_pic(loadname[0])

    # num_iterations defaults to 1 if it isn't defined
    num_iterations = 1
    if (iterations):
        num_iterations = iterations[0]

    # Iterate
    for ii in range(0 ,num_iterations):
        _save_iteration(savename, board, ii, num_iterations)
        board = iterate_board(board)
    _save_iteration(savename, board, num_iterations, num_iterations)

def main():
    parser = argparse.ArgumentParser(description='A weird RGB cellular automata')
    parser.add_argument("loadpic",
                        help="Load an image of the board from a filename",
                        type=str, nargs=1)
    parser.add_argument("--savepic","-s",
                        help="save an image to the directory, appended _xxx.png",
                        type=str, nargs=1)
    parser.add_argument("--iterate","-i",
                        help="iterate n times. Default 1.",
                        type=int, nargs=1)

    args = parser.parse_args()
    run(args.loadpic, args.iterate, args.savepic)


if __name__ == '__main__':
    main()
