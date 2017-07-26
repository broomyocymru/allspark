---
{%- for spark, data in data.sparks.iteritems() -%}
{% if data.software %}
- name: Setup {{ spark }}
  hosts: {{ spark }}
  become: true
  roles:
    - { role: {{data.software.name}} }
{% endif %}
{%- endfor -%}
