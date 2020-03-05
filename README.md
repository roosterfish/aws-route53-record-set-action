# AWS Route 53 Record Set

This GitHub Actions allows you to manage [AWS Route 53](https://aws.amazon.com/route53/) Record Sets. 

The naming is aligned with the official interface: https://docs.aws.amazon.com/cli/latest/reference/route53/change-resource-record-sets.html. There you can find possible variations for every Input this GitHub Action supports.

## Get started

A new AWS Route 53 Record Set can be created with the following workflow syntax:

```yaml
jobs:
  aws_route53:
    runs-on: ubuntu-latest
    steps:
      - name: "Create an A record set"
        uses: Roosterfish/aws-route53-record-set-action@master
        with: 
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws_route53_hosted_zone_id: ${{ secrets.AWS_ROUTE53_HOSTED_ZONE_ID }}
          aws_route53_rr_action: "CREATE"
          aws_route53_rr_name: "your-fqdn.example.com"
          aws_route53_rr_type: "A"
          aws_route53_rr_ttl: "300"
          aws_route53_rr_value: "1.2.3.4"
```

# GitHub Action Inputs

The behaviour of this Action can be modified with the following Inputs:

Name | Description | Choices | Required
--- | --- | --- | ---
`aws_access_key_id` | The AWS access key id | | yes
`aws_secret_access_key` | The AWS secret access key | | yes
`aws_route53_hosted_zone_id` | The id of the hosted zone | | yes
`aws_route53_rr_action` | The action that should be taken | `CREATE`, `DELETE`, `UPSERT` | yes
`aws_route53_rr_name` | The name of the record set | | yes
`aws_route53_rr_type` | The type of the record set | `SOA`, `A`, `TXT`, `NS`, `CNAME`, `MX`, `PTR`, `SRV`, `SPF`, `AAAA` | yes
`aws_route53_rr_ttl` | The TTL of the record set | | yes
`aws_route53_rr_value` | The value of the record set | | yes
`aws_route53_rr_comment` | A comment for the record set | | no
`aws_route53_wait` | Wait until the record set is fully settled in | `true`, `false` | no

## Supported Routing Policies

Currently this GitHub Actions supports the following Routing Policies of the AWS Route 53 service:

Name | Extra Variables
--- | ---
Basic | None

## License

The MIT License (MIT)

Copyright (c) 2020 Julian Pelizäus

### Used libraries

https://pypi.org/project/boto3/ licensed under [Apache License 2.0](https://github.com/boto/boto3/blob/develop/LICENSE)
