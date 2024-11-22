import sys
import argparse
import os

def build_decode_args(argparser: argparse.ArgumentParser):
    argparser.add_argument(
        'input',
        help = 'Input .vxn file.',
    )
    
    argparser.add_argument(
        '-o', '--output',
        dest = 'output',
        help = 'Output filename. Uses python format syntax, with {n} being stream number (as int), and {ext} as file extension.',
    )
    
    argparser.add_argument(
        '-s', '--stream',
        dest = 'stream_start',
        type = int,
        help = 'Choose specific stream to extract.',
    )
    
    argparser.add_argument(
        '-S', '--stream-select',
        dest = 'stream_end',
        type = int,
        help = 'Select the streams to extract.',
    )

def extract(args: argparse.Namespace):
    from .vxn import VXN
    
    audio = VXN(args.input)
    
    output = args.output
    if not output:
        output = f'{os.path.splitext(args.input)[0]}_{{n}}.{{ext}}'
    
    start = args.stream_start
    end = args.stream_end
    
    if start is not None and end is None:
        end = start
    elif start is None:
        start = 1
    
    start -= 1
    start = max(0, min(start, len(audio.streams) - 1))
    end = len(audio.streams) if end is None else max(0, min(end, len(audio.streams)))
    
    for n in range(start, end, 1 if end > start else -1):
        stream = audio.streams[n]
        stream.save(output.format(
            n = n,
            ext = stream.EXTENSION,
        ))
    

def extract_command(argparser: argparse.ArgumentParser | None = None):
    if argparser is None:
        argparser = argparse.ArgumentParser(
            description = 'Extract vxn files',
        )
    
    build_decode_args(argparser)
    args = parse_args(argparser)
    extract(args)
    

def parse_args(argparser: argparse.ArgumentParser):
    argv = sys.argv[1:]
    if len(argv) < 1:
        argparser.print_help()
        sys.exit()
    
    return argparser.parse_args(argv)
    

def main():
    argparser = argparse.ArgumentParser(
        description = 'Extract the raw data from vxn files.',
    )
    
    subparser = argparser.add_subparsers(
        title = 'commands',
        dest = 'command',
    )
    
    build_decode_args(subparser.add_parser(
        'extract',
        help = 'Extract vxn files',
        allow_abbrev = True,
        aliases = ['decode'],
    ))
    
    args = parse_args(argparser)
    match args.command:
        case 'extract':
            extract(args)

if __name__ == "__main__":
    main()
