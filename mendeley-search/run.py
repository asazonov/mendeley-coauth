from mendeley import Mendeley
import json
import argparse

mendeley = Mendeley("2640", "940Jj5NIz6xCPqqq")
session = mendeley.start_client_credentials_flow().authenticate()


def get_publications(query, size):
    total_papers = size
    current_papers = 0

    publications_list = list()
    unique_dois = set()

    catalog_search = session.catalog.search(query=query, view="all")
    search_page = catalog_search.list(page_size=100)

    while True:
        for doc in search_page.items:
            if doc.type == "journal" and doc.year >= 2000:
                if doc.identifiers is not None and "doi" in doc.identifiers:
                    doi = doc.identifiers["doi"]
                    # clean up
                    if doi.startswith("doi: "):
                        doi = doi.split("doi: ")[1]
                    if doi.startswith("DOI: "):
                        doi = doi.split("DOI: ")[1]
                    if doi.startswith("Doi "):
                        doi = doi.split("Doi ")[1]
                    if doi.startswith("http://dx.doi.org/"):
                        doi = doi.split("http://dx.doi.org/")[1]

                    # add to list
                    if doi not in unique_dois:
                        unique_dois.add(doi)
                        pub = dict()
                        pub["doi"] = doi
                        pub["title"] = doc.title
                        pub["abstract"] = doc.abstract \
                            if doc.abstract is not None else ""
                        pub["year"] = doc.year
                        pub["keywords"] = doc.keywords \
                            if doc.keywords is not None else list()
                        publications_list.append(pub)
                        current_papers += 1

        print("current papers:", current_papers)

        # continue to next page until we get enough papers
        if current_papers >= total_papers:
            break
        else:
            search_page = search_page.next_page

    return publications_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get research publications from Mendeley"
    )

    parser.add_argument(
        "--query", dest="query", type=str, help="Query"
    )

    parser.add_argument(
        "--size", dest="size", type=int, help="Number of publications"
    )

    args = parser.parse_args()

    publications = get_publications(args.query, args.size)

    with open("{}.json".format(args.query.replace(" ", "")), "w+") as fp:
        json.dump(publications, fp, indent=4)
