# Contents regenerated
{% for spark, data in data.sparks.iteritems() %}
module "{{ spark }}" {
  source    = "{{ data.infra.src }}"
  name      = "{{ spark }}"
  {% for pkey, pvalue in data.infra.params.iteritems() %}{{pkey}} = "{{pvalue}}"
  {% endfor %}
}
{% endfor %}
