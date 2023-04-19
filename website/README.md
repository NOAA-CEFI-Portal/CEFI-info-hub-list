## Website
Leveraged existing resources from https://github.com/noaa-fisheries-integrated-toolbox/toolbox_web_templating.

The webpages are built from the `website/` directory. 

* `Browse_config.json` - configuration for what resources to present on the webpage.
* `create_catalog_landing_page.py` - script to create the browse.html landing page
* `create_tool_landing_page.py` - script to create individual tool landing pages.
* `index.html` - html source for landing page. (links to browse.html created from `create_catalog_landing_page.py`)
* `static/main.css` - css control for website.

```bash
>cd website

>python create_catalog_landing_page.py
```