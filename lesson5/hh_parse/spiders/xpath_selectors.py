VACANCY_DATA = {
    'title': "//h1[@data-qa='vacancy-title']/text()",
    'salary': "//p[@class='vacancy-salary']//span[@data-qa='bloko-header-2']/text()",
    'description': "//div[@data-qa='vacancy-description']/descendant::text()",
    'skills': "//div[@class='bloko-tag-list']//span[@data-qa='bloko-tag__text']/text()",
    'author': "//a[@data-qa='vacancy-company-name']/@href"
}


COMPANY_DATA = {
    'name': "//span[@data-qa='company-header-title-name']/text()",
    'trusted': "//span[@class='company-header-title-trusted']",
    'site': "//a[@data-qa='sidebar-company-site']/@href",
    'description': "//div[@data-qa='company-description-text']/descendant::text()",
    'activity_areas': "//div[contains(text(), 'Сферы деятельности')]/../p//text()"
}