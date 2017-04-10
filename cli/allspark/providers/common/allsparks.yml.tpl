# Contents regenerated at {{data.updated_at}}
{% for spark, data in data.sparks.iteritems() %}
{% if data.software.src %}- src: {{ data.software.src }}{% endif %}
{% endfor %}
