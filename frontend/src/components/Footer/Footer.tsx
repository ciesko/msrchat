import { Caption1Strong, Link } from "@fluentui/react-components";
import { FooterStyles } from "./FooterStyles";
import { AppStateContext } from "../../state/AppProvider";
import { useContext } from "react";

function Footer() {
    const styles = FooterStyles();
    const appStateContext = useContext(AppStateContext)
    return (
        <div
            className={styles.footerContainer}
        >
            {
                appStateContext?.state.frontendSettings?.contact_us_link &&
                <>
                    <Link href={appStateContext?.state.frontendSettings?.contact_us_link || ''}>
                        <Caption1Strong className={styles.footerText}>Contact Us</Caption1Strong>
                    </Link>
                    <Caption1Strong className={styles.footerText}>|</Caption1Strong>
                </>
            }
            <Link href="https://www.microsoft.com/en-us/legal/terms-of-use" >
                <Caption1Strong className={styles.footerText}>Terms of Use</Caption1Strong>
            </Link>
            <Caption1Strong className={styles.footerText}>|</Caption1Strong>
            <Link href="https://go.microsoft.com/fwlink/?LinkId=521839" >
                <Caption1Strong className={styles.footerText}>Privacy & Cookies</Caption1Strong>
            </Link>
            <Caption1Strong className={styles.footerText}>|</Caption1Strong>
            <Caption1Strong className={styles.footerText}>
                &copy; {new Date().getFullYear()} Microsoft
            </Caption1Strong>
        </div>
    );
}

export default Footer;
