[
  {
    "name": "nginx",
    "image": "nginx",
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80,
        "protocol": "tcp",
        "name": "nginx",
        "appProtocol": "http"

      }
    ],
    "environment": [
      {
        "name": "ENV",
        "value": "${environment}"
      }
    ]
  }
]