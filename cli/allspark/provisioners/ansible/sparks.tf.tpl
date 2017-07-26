# Contents regenerated at {{data.updated_at}}
{% for spark, data in data.sparks.iteritems() -%}
module "{{ spark }}" {
  source    = "{{ data.infra.src }}"
  name      = "{{ spark }}"

  {%- if data.infra.params %}
  {% for pkey, pvalue in data.infra.params.iteritems()%}
  {{pkey}} = "{{pvalue}}"
  {%- endfor %}
  {%- endif %}

  {%- if data.infra.list_params %}
  {% for pkey, pvalue in data.infra.list_params.iteritems()%}
  {{pkey}} = {{pvalue|map('string')|list|tojson }}
  {%- endfor %}
  {%- endif %}
}

{%- if data.infra.outputs %}
{% for okey, ovalue in data.infra.outputs.iteritems()%}
output "{{okey}}" {
  value = "{{ovalue}}"
}
{%- endfor %}

{% endif %}
{% endfor %}
