---
{% for spark, data in data.sparks.iteritems() %}
- name: Setup {{ spark }}
  hosts: {{ spark }}
  roles:
    - { role: {{data.software.name}} {% for pkey, pvalue in data.software.params.iteritems() %}, {{pkey}}: "{{pvalue}}"{% endfor %} }
{% endfor %}
