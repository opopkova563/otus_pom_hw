def test_change_paper_type(browser, product_card_page):
    initial_paper_type = product_card_page.get_paper_type()
    product_card_page.change_paper_type(initial_paper_type)
    product_card_page.check_paper_type_changed(initial_paper_type)
