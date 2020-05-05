import argparse
import WebCrawler


def main():

    parser = argparse.ArgumentParser(description='Web screenshots')
    parser.add_argument("source", help="full URL or path to the file with URLs list you need to go", type=str)
    parser.add_argument("--depth", help="depth of walk through", type=int, default=0)
    parser.add_argument("--fullpage", help="sets the screenshot in full page format with saving several images",
                        action="store_true", default=False)
    args = parser.parse_args()

    crawler = WebCrawler.WebCrawler()
    crawler.depth_of_walk = args.depth
    crawler.is_fullpage = args.fullpage

    if args.source.startswith("http"):
        crawler.urls_need_to_go.append(args.source)
        crawler.walk_control()
    else:
        crawler.read_from_file(args.source)


if __name__ == '__main__':
    main()
