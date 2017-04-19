# Contents regenerated at {{data.updated_at}}
- src: https://github.com/broomyocymru/allspark.common
{% for spark, data in data.sparks.iteritems() %}
{% if data.software.src %}- src: {{ data.software.src }}{% endif %}
{% endfor %}
