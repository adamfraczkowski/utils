#!/bin/bash
dd=$(curl -Is google.com | grep Date:)
new_dd=${dd:6}
date -s """+$new_dd+"""