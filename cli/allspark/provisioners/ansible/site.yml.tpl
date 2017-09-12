---
{%- for spark, data in data.sparks.iteritems() -%}
{% if data.software %}
- name: Setup {{ spark }}
  hosts: {{ spark }}
  become: true
  roles:
    - { role: {{data.software.name}}{{data|software_role_params}}}
{% endif %}
{%- endfor -%}
