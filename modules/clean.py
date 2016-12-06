def destroy(is_list, args):
    if is_list:
        if args[0] is not None:
            if len(args[0]) != 0:
                for n in range(54):
                    args[0][n].destroy()
        for x in range(1, args.__len__()):
            if args[x] is not None:
                args[x].destroy()
    else:
        for x in range(0, args.__len__()):
            if args[x] is not None:
                args[x].destroy()
