import * as React from 'react';
import { HeaderStyles } from './HeaderStyles';
import { Button, Image, Link } from '@fluentui/react-components';
import { CosmosDBStatus } from '../../api';
import { HistoryButton } from '../common/Button';
import { AppStateContext } from '../../state/AppProvider';
import { useContext, useEffect, useState } from 'react';
import { PersonFeedback16Regular } from '@fluentui/react-icons';

export interface IHeaderProps {
    azureImageUrl: string;
    onShareClick: () => void;
    onHistoryClick: () => void;
    appStateContext: any;
}

export const Header: React.FunctionComponent<IHeaderProps> = (props: React.PropsWithChildren<IHeaderProps>) => {
    const styles = HeaderStyles();
    const appStateContext = useContext(AppStateContext);

    const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 600);

    useEffect(() => {
        const checkSize = () => setIsSmallScreen(window.innerWidth < 600);

        window.addEventListener('resize', checkSize);

        // Cleanup function
        return () => window.removeEventListener('resize', checkSize);
    }, []);

    return (
        <div className={styles.container}>
            <div className={styles.titleContainer}>
                <Image
                    src={props.azureImageUrl}
                    aria-hidden="true"
                    className={styles.logoImage}
                />
                <span className={styles.verticalBar}>|</span>
                <Link href="/" className={styles.headerTitle}>
                    {appStateContext?.state?.frontendSettings?.site_title}
                </Link>
            </div>
            <div className={styles.rightCommandBar}>
                {(props.appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured) &&
                    <HistoryButton onClick={props.onHistoryClick} text={props.appStateContext?.state?.isChatHistoryOpen ? "Hide chat history" : "Show chat history"} />
                }
                {
                    appStateContext?.state.frontendSettings?.submit_feedback_url &&
                    <Link
                        title="Submit feedback"
                        href={appStateContext?.state.frontendSettings?.submit_feedback_url}
                    >
                        {isSmallScreen ? <PersonFeedback16Regular /> : 'Submit feedback'}
                    </Link>
                }
            </div>
        </div>
    );
};