# GET not support body

That's true for OpenAPI 3.0, but seems to be changed in 3.1 as this PR suggests. The same change was removed from 3.0 only because it did't fit the semantics of a patch release

According to the PR, 3.1 will read as follows, which is in-line with RFC 7231.

[Fast-api issue](https://github.com/tiangolo/fastapi/issues/2004)
[[fastapi]]
[[http]]