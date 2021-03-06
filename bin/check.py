#!/usr/bin/python
import sys
import logging
import click
from gsl.utils import yield_packages
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@click.command()
@click.argument('galaxy_package_file')
def main(galaxy_package_file):
    with open(galaxy_package_file, 'r') as handle:
        retcode = 0
        identifiers = set()
        keys = ['id', 'version', 'platform', 'arch', 'url', 'sha', 'size',
                'alt_url', 'comment']

        for ld, lineno, line, extraret in yield_packages(handle, retcode=retcode, meta=True):
            if extraret > 0:
                retcode = extraret
            try:
                for x in keys[0:6]:
                    if ld.get(x, '').strip() == '':
                        log.error("[%s] Empty %s", lineno, x)
                        retcode = 1

                if ld['platform'] not in ('linux', 'windows', 'darwin', 'src'):
                    log.error("[%s] Unknown platform %s", lineno, ld['platform'])
                    retcode = 1

                if ld['arch'] not in ('x32', 'x64', 'all'):
                    log.error("[%s] Unknown architecture %s", lineno, ld['arch'])
                    retcode = 1

                if len(ld['sha']) != 64:
                    log.error("[%s] Bad checksum %s", lineno, ld['sha'])
                    retcode = 1

                platform_id = (ld['id'], ld['version'], ld['platform'], ld['arch'])
                if platform_id in identifiers:
                    log.error("[%s] identifier is not unique: '%s'", lineno, platform_id)
                    retcode = 1
                else:
                    identifiers.add(platform_id)

            except:
                log.error("[%s] Line not tabbed properly", lineno)
                retcode = 1
        sys.exit(retcode)


if __name__ == '__main__':
    main()
