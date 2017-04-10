# Contents regenerated at {{data.updated_at}}
{% for spark, data in data.sparks.iteritems() %}
module "{{ spark }}" {
  source    = "{{ data.infra.src }}"
  name      = "{{ spark }}"
  {% for pkey, pvalue in data.infra.params.iteritems() %}{{pkey}} = "{{pvalue}}"
  {% endfor %}
}
{% if data.infra.outputs %}
{% for okey, ovalue in data.infra.outputs.iteritems() %}
output "{{okey}}" {
  value = "{{ovalue}}"
}
{% endfor %}
{% endif %}

{% endfor %}
