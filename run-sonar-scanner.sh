docker run \
    --rm \
    -e SONAR_HOST_URL="http://172.17.0.2:9000"  \
    -e SONAR_TOKEN="sqp_a1625bbc3e07639d7e06f515b43e74572b333332" \
    -v "$PWD:/usr/src" \
    sonarsource/sonar-scanner-cli