import soundfile
import pathlib


def validated_path(path):
    path = pathlib.Path(path)
    if not path.exists():
        raise ValueError("file %s does not exist" % path)
    return path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type=validated_path, help="audio file to split"
    )
    parser.add_argument(
        "--duration", default=60, type=int,
        help="A duration of clips in second"
    )
    parser.add_argument(
        "--output", default=None, type=pathlib.Path,
        help="An output path. The default is the same directory of the input file"
    )
    args = parser.parse_args()

    # read blocks
    sfobj = soundfile.SoundFile(args.file)
    fs = sfobj.samplerate
    blocksize = int(fs * args.duration)

    output = args.output
    if output is None:
        output = args.file.with_suffix("")
    output.mkdir(exist_ok=True, parents=True)

    for index, block in enumerate(sfobj.blocks(blocksize)):
        print("Writing the clip %d..." % index)
        soundfile.write(
            output / ("%05d.wav" % index), block, fs
        )
    print("""
    Input audio file : %s
    Number of files  : %d
    Output directory : %s
    """ % (args.file.absolute(), index, output.absolute()))

    print("Succeeded.")
