# Keep Chirpy's canonical URLs and JSON-LD, extending only missing metadata.
require 'nokogiri'
require 'json'

Jekyll::Hooks.register [:pages, :documents], :pre_render do |page|
  if page.data['layout'] == 'home' && page.site.active_lang == 'pt-BR'
    page.data['lang'] = 'pt-BR'
    page.data['title'] = 'Engenharia de Software e IA'
    page.data['seo_title'] = 'Engenharia de Software e IA | Marcelo Miyake'
    page.data['description'] = 'Artigos sobre agentes de programação com IA, arquitetura de software e desenvolvimento backend, com práticas aplicáveis e evidências.'
  end

  next unless %w[tag category].include?(page.data['layout'])
  next if page.data['description']

  topic = page.to_liquid['title']
  if (page.data['lang'] || page.site.active_lang) == 'pt-BR'
    page.data['lang'] = 'pt-BR'
    page.data['description'] = "Explore artigos sobre #{topic} de Marcelo Miyake, com orientações práticas sobre agentes de programação com IA, arquitetura de software e práticas de desenvolvimento."
  else
    page.data['description'] = "Explore articles about #{topic} by Marcelo Miyake, with practical guidance on AI coding agents, software architecture, and development practices."
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |page|
  next unless page.output_ext == '.html'

  html = Nokogiri::HTML(page.output)
  if page.data['seo_title']
    html.at_css('title').content = page.data['seo_title']
  end

  # Post cards are subsections of the home page, not separate page headings.
  if page.data['layout'] == 'home'
    if page.site.active_lang == 'pt-BR'
      title = page.data['title'] || 'Engenharia de Software e IA'
      description = page.data['description']
      localized_home_url = [page.site.config['url'], page.site.baseurl].map(&:to_s).join.sub(%r{/+\z}, '') + '/pt-BR/'
      html.at_css('meta[property="og:title"]')&.[]=('content', title)
      html.at_css('meta[name="twitter:title"]')&.[]=('content', title)
      html.at_css('meta[property="og:locale"]')&.[]=('content', 'pt_BR')
      html.at_css('meta[property="og:url"]')&.[]=('content', localized_home_url)
      html.css('meta[name="description"], meta[name="twitter:description"], meta[property="og:description"]').each do |meta|
        meta['content'] = description if description
      end

      if (structured_data = html.at_css('script[type="application/ld+json"]'))
        website = JSON.parse(structured_data.content)
        website['description'] = description if description
        website['headline'] = title
        website['url'] = localized_home_url
        structured_data.content = JSON.generate(website)
      end
    end

    html.css('#post-list h1').each { |heading| heading.name = 'h2' }
    if (list = html.at_css('#post-list'))
      heading = Nokogiri::XML::Node.new('h1', html)
      heading['class'] = 'mb-4'
      heading.content = page.data['title'] || page.site.config['title']
      list.add_previous_sibling(heading)
    end
  end

  page.output = html.to_html
end
