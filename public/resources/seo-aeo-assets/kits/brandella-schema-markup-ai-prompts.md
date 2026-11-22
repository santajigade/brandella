# Schema Markup: AI prompt pack

From Brandella Journal, free to use. Full guide: https://brandella.in/resources/seo-aeo-assets/schema-markup/

Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini. Always check the output against real data.

## 1. Choose the right schema type

```
Here is a summary of my page: [URL, page type, main content]. Which schema.org type best describes the main content, and does
Google show a rich result for it today? List any secondary types worth adding, like BreadcrumbList. Only suggest types that
describe content visible on the page.
```

## 2. JSON-LD from page text

```
Here is the visible text of my [page type] page: [paste]. Write JSON-LD for the [type] type using only facts that appear in this text.
Include Google's required properties and the recommended ones the text supports. Do not invent prices, ratings, dates or names.
```

## 3. Audit existing markup

```
Here is the JSON-LD on my page: [paste]. And here is the visible page text: [paste]. List every value in the markup that is not on the
page or differs from it, every required property Google needs for this type that is missing, and any property that looks invented.
```

## 4. Fix Rich Results Test errors

```
The Rich Results Test shows these errors and warnings for my page: [paste]. Here is my markup: [paste]. Explain each issue in plain
words and give me the corrected JSON-LD.
```

## 5. Product markup from a catalogue row

```
Here is one row of my product data with these columns: [paste]. Write Product JSON-LD with name, image, description, brand, sku and
an Offer with price, priceCurrency and availability. Then turn it into a template with placeholders I can fill from each row.
```

## 6. Article markup with author

```
Write BlogPosting JSON-LD for my article "[title]" by [author] ([author profile URL]), published [date], updated [date], with this
main image: [URL]. Use ISO 8601 dates with my time zone ([zone]). Add only properties I gave you.
```

## 7. LocalBusiness markup

```
Write JSON-LD for my [business type] using the most specific schema.org subtype. Name: [name]. Address: [address]. Phone: [phone].
Hours: [hours]. Website: [URL]. Coordinates: [lat, long]. Use openingHoursSpecification for the hours. No reviews or ratings.
```

## 8. Event markup

```
Write Event JSON-LD for "[event]" on [date and time] at [venue and full address], tickets [price and currency] at [URL],
organised by [organiser]. Add eventStatus and eventAttendanceMode. Flag anything Google requires that I did not give you.
```

## 9. Breadcrumb markup

```
My page [URL] sits under this trail: [Home > Section > Page, with URLs]. Write BreadcrumbList JSON-LD that matches the breadcrumb
shown on the page. Leave item off the last crumb if it is the current page.
```

## 10. Video markup

```
Write VideoObject JSON-LD for my video "[title]": description [text], thumbnail [URL], upload date [date], duration [minutes and seconds],
file URL [URL], embed URL [URL]. Convert the duration to ISO 8601.
```

## 11. Organization and site name

```
Write Organization JSON-LD for my home page and a separate WebSite block for the site name. Name: [name]. Other name: [short name].
URL: [URL]. Logo: [URL]. Official profiles: [URLs]. Contact: [email, phone]. Address: [address]. No reviews or ratings.
```

## 12. Author profile page

```
Write ProfilePage JSON-LD for the author page of [name] at [URL]: [short bio], photo [URL], profiles [URLs], page created [date],
updated [date]. The person should be the mainEntity.
```

## 13. Is this review markup allowed

```
I want to add review stars with this markup: [paste]. The reviews are about [my own business or another product or business] and
they come from [source]. Based on Google's review snippet guidelines, is this eligible? If not, what should I do instead?
```

## 14. Retired rich results check

```
My site uses these schema types: [list]. Which of them no longer produce a rich result in Google Search, and which still do?
For the retired ones, should I keep, change or remove the markup? Base your answer on Google's current documentation and say what to verify.
```

## 15. Microdata to JSON-LD

```
Here is the Microdata on my page: [paste HTML]. Convert it to an equivalent JSON-LD block with the same values, and list the HTML
attributes I can remove once the JSON-LD is live.
```

## 16. Template wide markup plan

```
My site has these templates: [list with page counts]. Suggest the schema types for each template, the data fields each needs from my
CMS, and the order to roll them out based on which still earn a Google result.
```

## 17. Explain my schema audit

```
Here are the key numbers and top issues from my schema audit: [paste Dashboard numbers and Schema Lab priorities]. Explain in plain
words what to fix first, what can wait and what I can ignore.
```

## 18. Workflow 1 of 5: brief the assistant

```
You are my structured data editor. My site: [site], about [topic]. Rules: JSON-LD only, the most specific schema.org type, every
Google required property, recommended properties only when the page shows the fact, never invent values, no reviews about my own
business. Confirm, then wait for my page.
```

## 19. Workflow 2 of 5: the page

```
Here is the page: URL [URL], page type [type], visible text [paste], and these facts that appear on it: [prices, dates, names, address,
hours]. Tell me which schema types fit this page and which Google rich results they can earn.
```

## 20. Workflow 3 of 5: the JSON-LD

```
Write the JSON-LD for the main type you chose, plus BreadcrumbList if the page shows a breadcrumb. Use only the facts I gave you.
After the code, list each Google required property and where its value comes from on the page.
```

## 21. Workflow 4 of 5: pressure test

```
Check your JSON-LD line by line: is every value visible on the page, are all required properties present, is the type right for the page,
are dates in ISO 8601 with a time zone, and is anything invented or self serving? Return the corrected code.
```

## 22. Workflow 5 of 5: row for Excel

```
Turn the final markup into a row with tabs between columns for my Schema Lab: URL, Page type, Schema type, Format (JSON-LD),
Properties in the markup (comma separated property names, nested ones with a dot), Matches the visible page (Yes),
Rich Results Test (Not tested), Search Console report (blank), Blocked for Googlebot (No), Values last checked ([today]), Notes.
```
