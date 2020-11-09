import argparse
import os

from api_client import ShopifyApiClient


def save_products(args):
    client.saves_all_products_by_fields(extension=args.format,
                                        fields=['id', 'title', 'body_html', 'vendor', 'created_at', 'variants'],
                                        nested_fields_to_return={"variants": ["id", "sku", "title", "price"]},
                                        path=args.path_directory)
    return f"Products saved:\n{args.path_directory}"


def update_products(args):
    client.update_products_from_file(path_to_file=args.path_file)
    return "Products updated"


def collect_args():
    parser = argparse.ArgumentParser(description="Operations on Shopify Api Client",
                                     epilog="Modify fields and nested_fields_to_return in script to change behavior")
    subparsers = parser.add_subparsers(help='Commands')

    parser_save = subparsers.add_parser('save', help='Saves all products in file')
    parser_save.set_defaults(func=save_products)
    parser_save.add_argument('-f', '--format', choices=client.available_extensions, required=True,
                             help="File format to save data")
    parser_save.add_argument("-pd", "--path-directory",
                             default=os.getcwd(),
                             help="Path to directory to save file, default current directory")

    parser_update = subparsers.add_parser('update', help='Update products by given file')
    parser_update.set_defaults(func=update_products)
    parser_update.add_argument("-pf", "--path-file", required=True,
                               help="Path to file with data")

    return parser.parse_args()


if __name__ == "__main__":
    client = ShopifyApiClient()
    args = collect_args()
    print(args.func(args))
