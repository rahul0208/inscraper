#!/usr/bin/env python3

import re
import time
import argparse
from core.scraper import Scraper
from core.transformer import Transformer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape data from search engine LinkedIn profiles.")

    # Allow a user to scrape names or just convert an already generated list of names
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--company", type=str, help="Target company to search for LinkedIn profiles.")
    parser.add_argument("-d", "--depth",   type=int, help="Number of pages to search each search engine. Default: 5", default=5)
    parser.add_argument("-t", "--timeout", type=int, help="Specify request timeout. Default: 25", default=25)
    parser.add_argument("-o", "--output",  type=str, help="Directory to write username files to.")
    parser.add_argument("--cookie",        type=str, help="File containing Google CAPTCHA bypass cookies")
    parser.add_argument("--proxy",         type=str, help="Proxy to pass traffic through: <ip:port>")
    parser.add_argument("--debug",         action="store_true", help="Enable debug output.")
    args = parser.parse_args()

    start = time.time()

    output = args.output if args.output else "./"

    if args.company:
        scraper = Scraper(args.company, cookies=args.cookie, depth=args.depth, timeout=args.timeout, proxy=args.proxy)
        scraper.loop.run_until_complete(scraper.run())
        print("\n\n[+] Names Found: %d" % len(scraper.employees))
        print("[*] Writing names to the following directory: %s" % output)
        with open("%s/names.txt" % (output), 'a') as f:
            for name in scraper.employees:
                f.write("%s\n" % name)

    elapsed = time.time() - start
    if args.debug: print("\n[DEBUG] %s executed in %0.4f seconds." % (__file__, elapsed))