import unbmp


def test_check_filetype() -> None:
    fname = "abcABC123.bMp"
    ftype = "bmP"

    def all_lower(fname: str, ftype: str) -> None:
        assert unbmp.check_filetype(fname.lower(), ftype) is True
        assert unbmp.check_filetype(fname.lower(), ftype.lower()) is True
        assert unbmp.check_filetype(fname.lower(), ftype.upper()) is True

    def all_upper(fname: str, ftype: str) -> None:
        assert unbmp.check_filetype(fname.upper(), ftype) is True
        assert unbmp.check_filetype(fname.upper(), ftype.lower()) is True
        assert unbmp.check_filetype(fname.upper(), ftype.upper()) is True

    def mixed_case(fname: str, ftype: str) -> None:
        assert unbmp.check_filetype(fname, ftype) is True
        assert unbmp.check_filetype(fname, ftype.lower()) is True
        assert unbmp.check_filetype(fname, ftype.upper()) is True

    def no_dot(ftype: str) -> None:
        fname_nodot = "abcABC123bMp"
        assert unbmp.check_filetype(fname_nodot, ftype) is False
        assert unbmp.check_filetype(fname_nodot, ftype.lower()) is False
        assert unbmp.check_filetype(fname_nodot, ftype.upper()) is False

    def ends_with_dot(ftype: str) -> None:
        fname_enddot = "abcABC123bMp."
        assert unbmp.check_filetype(fname_enddot, ftype) is False
        assert unbmp.check_filetype(fname_enddot, ftype.lower()) is False
        assert unbmp.check_filetype(fname_enddot, ftype.upper()) is False

    all_lower(fname, ftype)
    all_upper(fname, ftype)
    mixed_case(fname, ftype)
    no_dot(ftype)
    ends_with_dot(ftype)


def test_get_conv_fname() -> None:
    fname = "abcABC123.bmp"
    fname_w_path = "/home/user/Pictures/cool\ pictures/bmp/" + fname
    dest_ext = "png"
    output_dir = "/home/user/Pictures/cool\ pictures/png/"

    def no_path_no_output_dir(fname: str, dest_ext: str) -> None:
        goal_string = fname.split('.')[0] + '.' + dest_ext

        assert unbmp.get_conv_fname(fname, dest_ext) == goal_string

    def no_path_output_dir(fname: str, dest_ext: str, output_dir: str) -> None:
        goal_string = output_dir + fname.split('.')[0] + '.' + dest_ext

        assert unbmp.get_conv_fname(fname, dest_ext, output_dir) == goal_string

    def path_no_output_dir(fname: str, dest_ext: str) -> None:
        goal_string = fname.split('.')[0] + '.' + dest_ext

        assert unbmp.get_conv_fname(fname, dest_ext) == goal_string

    def path_output_dir(fname: str, dest_ext: str, output_dir: str) -> None:
        goal_string = output_dir + fname.split('/')[-1].split('.')[0] + '.'\
            + dest_ext

        assert unbmp.get_conv_fname(fname, dest_ext, output_dir) == goal_string

    no_path_no_output_dir(fname, dest_ext)
    no_path_output_dir(fname, dest_ext, output_dir)
    path_no_output_dir(fname_w_path, dest_ext)
    path_output_dir(fname, dest_ext, output_dir)
