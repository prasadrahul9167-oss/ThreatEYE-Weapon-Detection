# Security Policy

## Supported Versions

Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1. **DO NOT** open a public issue
2. Email security details to: security@threateye.example.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Based on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   # Backend
   pip install --upgrade -r requirements.txt
   
   # Frontend
   yarn upgrade
   ```

2. **Use HTTPS Only**
   - Never deploy without SSL/TLS
   - Webcam requires secure context

3. **Environment Variables**
   - Never commit .env files
   - Use strong database passwords
   - Rotate credentials regularly

4. **Network Security**
   - Use firewall rules
   - Restrict MongoDB access
   - Implement rate limiting

5. **Authentication**
   - Add authentication for production
   - Use JWT tokens with expiration
   - Implement role-based access

### For Developers

1. **Code Review**
   - All changes require review
   - Security-focused code reviews
   - Use automated security scanners

2. **Dependencies**
   - Regular dependency audits
   - Use `pip-audit` for Python
   - Use `yarn audit` for Node.js

3. **Input Validation**
   - Validate all user inputs
   - Sanitize data before storage
   - Use Pydantic models

4. **Error Handling**
   - Don't expose stack traces
   - Log security events
   - Use generic error messages

## Known Security Considerations

### Camera Access
- Requires user permission
- Only works over HTTPS
- No video recording by default

### API Endpoints
- Currently open (add auth in production)
- Rate limiting recommended
- CORS configured (review for production)

### Database
- MongoDB should not be public
- Use authentication
- Enable encryption at rest

### Model Files
- YOLOv8 models auto-download
- Verify checksums
- Use official sources only

## Security Checklist for Production

- [ ] HTTPS enabled with valid certificate
- [ ] Authentication implemented
- [ ] Rate limiting configured
- [ ] Database authentication enabled
- [ ] Firewall rules configured
- [ ] CORS properly restricted
- [ ] Environment variables secured
- [ ] Logging and monitoring enabled
- [ ] Regular backups configured
- [ ] Dependencies up to date
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] Error messages sanitized

## Compliance

### Data Privacy

- **GDPR**: No personal data stored by default
- **CCPA**: Comply with data rights requests
- **Video Data**: Not recorded, only analyzed

### Usage Guidelines

- Inform users about camera usage
- Display privacy notice
- Comply with local surveillance laws
- Obtain necessary consents

## Vulnerability Disclosure

We believe in responsible disclosure and will:

1. Acknowledge receipt of vulnerability report
2. Investigate and verify the issue
3. Develop and test a fix
4. Release security update
5. Credit reporter (if desired)
6. Publish security advisory

## Security Updates

Security updates are released as:
- Patch versions for minor issues
- Minor versions for moderate issues
- Immediate hotfix for critical issues

Subscribe to releases to get notifications.

---

**Last Updated**: February 11, 2026
