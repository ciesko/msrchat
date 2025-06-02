import * as React from 'react';
import { SuggestionButtonStyles } from './SuggestionButtonStyles';
import { Button, Title3 } from '@fluentui/react-components';
import { AppStateContext } from '../../state/AppProvider';
import { useContext } from 'react';

export interface ISuggestionButtonsProps {
    onButtonClick: (questionText: string) => void;
}

export const SuggestionButtons: React.FunctionComponent<ISuggestionButtonsProps> = (props: React.PropsWithChildren<ISuggestionButtonsProps>) => {
    const styles = SuggestionButtonStyles();
    const appStateContext = useContext(AppStateContext)

    return (
        <div className={styles.container}>
            <Title3 className={styles.prompt}><i>{appStateContext?.state.frontendSettings?.frontpage_question_heading}</i></Title3>
            <div className={appStateContext?.state.frontendSettings?.frontpage_vertical_questions ? styles.questionsContainerVertical : styles.questionsContainerHorizontal}>
                {
                    appStateContext?.state.frontendSettings?.frontpage_questions?.map((questionText, index) => {
                        return (
                            appStateContext?.state.frontendSettings?.frontpage_vertical_questions ?
                                <Button appearance='subtle' size='small' key={index} onClick={() => props.onButtonClick(questionText)}>{questionText}</Button>
                                :
                                <Button appearance='secondary' className={styles.button} size='medium' key={index} onClick={() => props.onButtonClick(questionText)}>{questionText}</Button>
                        )
                    })
                }
            </div>
        </div>
    );
};