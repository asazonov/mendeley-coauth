from mendeley import Mendeley

mendeley = Mendeley("2640", "940Jj5NIz6xCPqqq")
session = mendeley.start_client_credentials_flow().authenticate()

catalog_search = session.catalog.advanced_search(title="computer vision",
                                                 view="all")
for catalog_doc in catalog_search.iter(5):
    print("title:", catalog_doc.title, "id:", catalog_doc.id)
